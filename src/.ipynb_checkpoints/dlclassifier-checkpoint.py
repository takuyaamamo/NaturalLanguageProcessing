import chainer
# 活性化関数等を管理する関数
import chainer.functions as F
# BiasとWeightを管理する関数
import chainer.links as L
import numpy
from chainer import training
from chainer.training import extensions
import sys
sys.path.append('/home/vagrant/chainer/examples/text_classification')
import nets
import nlp_utils

# 継承クラスの作成、class名はEncoder,別ファイルのchainer.Chainを継承する
class Encoder(chainer.Chain):
    
    # def __init__はコンストラクタ
    # 中には、どのように生成するか、どのようなデータを持たせるかなど、といった情報を定義する
    def __init__(self, w):
        # super(Encoder, self).__init__()で別ファイルのスーパークラス（chainer.Chain）のメソッドを呼び出すことが出来る。
        super(Encoder, self).__init__()
        # 300はWord2Vecの次元数
        self.out_units = 300
        
        # with構文でファイルを扱う
        # Chainクラスで重みの更新がされるのは self.init_scope()内に書いている linkオブジェクト
        with self.init_scope():
            self.embed = lambda x: F.embed_id(x, w)
            # 学習するLSTMの形を設定する
            self.encoder = L.NStepLSTM(n_layers=1, in_size=300, out_size=self.out_units, dropout=0.5)
    
    # 単語のID列をWord2Vecのベクトル列のデータに変換し、LSTMにわたす
    def forward(self, xs):
        exs = nets.sequence_embed(self.embed, xs)
        last_h, last_c, ys = self.encoder(None, None, exs)
        return last_h[-1]
    
# trainでモデルの学習を行う
def train(labels, features, w):
    # set型、集合型に変換する
    n_class = len(set(labels))
    print(f'# data: {len(features)}')
    print(f'# class: {n_class}')
    
    # 学習用データをchainerのiteratorの形にしておく
    pairs = [(vec, numpy.array([cls], numpy.int32)) for vec, cls in zip(features, labels)]
    train_iter = chainer.iterators.SerialIterator(pairs, batch_size=16)
    
    # 学習するモデルをちゃいねｒのサンプルプログラムのTextClassifierクラスを用いて設定する
    # 二値分類であるためカテゴリ数には2を指定、モデルはEncoderクラスのLSTMを指定する
    model = nets.TextClassifier(Encoder(w), n_class)
    
    # 最適化にはAdamを選択
    # ニューラルネットの学習方法を指定します。SGDは最も単純なものです。
    optimizer = chainer.optimizers.Adam()
    # 学習させたいパラメータを持ったChainをオプティマイザーにセットします。
    optimizer.setup(model)
    optimizer.add_hook(chainer.optimizer.WeightDecay(1e-4))
    
    # optimizerを使用してupdatersでパラメータを更新する
    updater = training.updaters.StandardUpdater(train_iter, optimizer, converter=convert_seq)
    # Trainerを用意する。updaterを渡すことで使える。epochを指定する。outはデータを保存する場所。
    trainer = training.Trainer(updater, (8, 'epoch'), out='./result/dl')
    
    # 下記で学習経過を確認する
    trainer.extend(extensions.LogReport())
    trainer.extend(extensions.PrintReport(['epoch', 'main/loss', 'main/accuracy', 'elapsed_time']))
    
    # 学習スタート
    trainer.run()
    return model

# 分類の実行
def classify(features, model):
    with chainer.using_config('train', False), chainer.no_backprop_mode():
        # chainerのpredict関数からは各カテゴリに対数確率値が帰ってくる
        prob = model.predict(features, softmax=True)
    answers = model.xp.argmax(prob, axis=1)
    return answers

# Word2Vecを元に作成したボキャブラリを用いて、単語を単語のIDに変換する
def convert_into_features_using_vocab(sentences, vocab):
    contents = []
    for doc_id, sent, tokens in sentences:
        features = [token['lemma'] for token in tokens]
        contents.append(features)
    features = transform_to_array(contents, vocab, with_label=False)
    return features

# nlp_utilsが読み込めないため持ってくる
import collections
import io

import numpy

import chainer
from chainer.backends import cuda


def split_text(text, char_based=False):
    if char_based:
        return list(text)
    else:
        return text.split()


def normalize_text(text):
    return text.strip().lower()


def make_vocab(dataset, max_vocab_size=20000, min_freq=2):
    counts = collections.defaultdict(int)
    for tokens, _ in dataset:
        for token in tokens:
            counts[token] += 1

    vocab = {'<eos>': 0, '<unk>': 1}
    for w, c in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
        if len(vocab) >= max_vocab_size or c < min_freq:
            break
        vocab[w] = len(vocab)
    return vocab


def read_vocab_list(path, max_vocab_size=20000):
    vocab = {'<eos>': 0, '<unk>': 1}
    with io.open(path, encoding='utf-8', errors='ignore') as f:
        for l in f:
            w = l.strip()
            if w not in vocab and w:
                vocab[w] = len(vocab)
            if len(vocab) >= max_vocab_size:
                break
    return vocab


def make_array(tokens, vocab, add_eos=True):
    unk_id = vocab['<unk>']
    eos_id = vocab['<eos>']
    ids = [vocab.get(token, unk_id) for token in tokens]
    if add_eos:
        ids.append(eos_id)
    return numpy.array(ids, numpy.int32)


def transform_to_array(dataset, vocab, with_label=True):
    if with_label:
        return [(make_array(tokens, vocab), numpy.array([cls], numpy.int32))
                for tokens, cls in dataset]
    else:
        return [make_array(tokens, vocab)
                for tokens in dataset]


def convert_seq(batch, device=None, with_label=True):
    def to_device_batch(batch):
        if device is None:
            return batch
        elif device < 0:
            return [chainer.dataset.to_device(device, x) for x in batch]
        else:
            xp = cuda.cupy.get_array_module(*batch)
            concat = xp.concatenate(batch, axis=0)
            sections = numpy.cumsum([len(x)
                                     for x in batch[:-1]], dtype=numpy.int32)
            concat_dev = chainer.dataset.to_device(device, concat)
            batch_dev = cuda.cupy.split(concat_dev, sections)
            return batch_dev

    if with_label:
        return {'xs': to_device_batch([x for x, _ in batch]),
                'ys': to_device_batch([y for _, y in batch])}
    else:
        return to_device_batch([x for x in batch])