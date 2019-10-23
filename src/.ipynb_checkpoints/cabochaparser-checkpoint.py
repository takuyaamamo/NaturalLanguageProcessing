# 正規表現操作を行うライブラリ
import re
# CaboChaをインポート
import CaboCha

# CaboChaをインスタンス化
cabocha = CaboCha.Parser('-n1')
# 。!<_EOS_>を文の文末としている為正規表現にまとめ文の区切り時に使用する。
ptn_sentence = re.compile(r'(^|。|！|<__EOS__>)\s*(.+?)(?=(。|！|<__EOS__>))', re.M)

# 正規表現を使用して文末で分割する関数定義
def split_into_sentences(text):
    sentences = []
    # 正規表現に従ってテキストを区切りmに出力していく。
    for m in ptn_sentence.finditer(text):
        sentences.append((m.group(2), m.start(2)))
    return sentences

# 係り受け木を構築し、ディキショナリで返す関数定義
def parse_sentence(sentence_str, sentence_begin, chunks, tokens):
    # CaboChaを呼び出し係り受け木を取得する
    tree = cabocha.parse(sentence_str)

    offset = sentence_begin
    chunk_id_offset = len(chunks)
    text = sentence_str
    
    # チャンク（文節に相当する塊）ごとにforを回す。
    for i in range(tree.chunk_size()):
        chunk = tree.chunk(i)
        chunk_begin = None
        
        # 各チャンクに含まれるトークン（単語）の情報を出力する
        for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
            token = tree.token(j)
            features = token.feature.split(',')
            # トークンの開始位置、何文字目から単語が始まるか
            token_begin = text.find(token.surface) + offset
            # トークンの終了位置、何文字目に単語が終わるか
            token_end = token_begin + len(token.surface)
            
            # チャンク内の最初のトークン開始位置
            if chunk_begin is None:
                chunk_begin = token_begin

            tokens.append({
                'begin': token_begin,
                'end':   token_end,
                # lemmaは単語の原型
                'lemma': features[-3],
                # POS（Part-of Speech）はその単語の品詞
                'POS':   features[0],
                # POSをより細かく分類したもの
                'POS2':  features[1],
                # NE(Named Entity)固有表現かどうか、人名・組織名・地名・日付・時間など
                'NE':    token.ne,
            })

            text = text[token_end-offset:]
            offset = token_end

        # チャンク内の最後のトークン終了位置
        chunk_end = token_end
        if chunk.link == -1:
            link = -1
        else:
            # チャンクのIDを手前に出現したチャンス数だけずらす
            link = chunk.link + chunk_id_offset
        chunks.append({
            'begin':    chunk_begin,
            'end':      chunk_end,
            'link':     ('chunk', link),
        })

# 上記２つの関数を利用し文の情報を生成する関数定義
def parse(text):
    sentences = []
    chunks = []
    tokens = []
    sentence_begin = 0

    # 正規表現を使用して文末で分割
    for sentence_str, sentence_begin in split_into_sentences(text):
        # 係り受け木を構築し、ディキショナリで返す
        parse_sentence(sentence_str, sentence_begin, chunks, tokens)
        sentence_end = chunks[-1]['end']

        sentences.append({
            'begin':    sentence_begin,
            'end':      sentence_end,
        })

    return sentences, chunks, tokens
