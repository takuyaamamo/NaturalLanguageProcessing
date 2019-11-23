from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer

# BoW形式の特徴量に変換する
# gensimのCountVectorizerをanalyzer='word'で実行する事で、半角スペースを単語区切りとみなしたBoWベクトルを作成できる
def vectorize(contents, vocab=None):
    vectorizer = CountVectorizer(analyzer='word', vocabulary=vocab)
    vecs = vectorizer.fit_transform(contents)
    vocab = vectorizer.vocabulary_
    return vecs, vocab

# テキストから特徴量を抽出する関数
def convert_into_features(sentences, vocab=None):
    contents = []
    for doc_id, sent, tokens in sentences:
        # 単語で分割
        lemmas = [token['lemma'] for token in tokens if token['POS'] in ['名詞', '動詞']]
        # 半角スペースで区切り
        content = ' '.join(lemmas)
        contents.append(content)
    # 入力されたテキストに含まれる単語をもとにしたボキャブラリを自動で作成している
    features, vocab = vectorize(contents, vocab=vocab)
    return features, vocab

# 学習の際も分類の際も同じvocabを使用する為
def convert_into_features_using_vocab(sentences, vocab):
    features, _ = convert_into_features(sentences, vocab)
    return features

# 学習
def train(labels, features):
    model = svm.LinearSVC()
    model.fit(features, labels)
    return model

# 分析結果を返す
def classify(features, model):
    predicts = model.predict(features)
    return predicts