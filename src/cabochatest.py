# かぼちゃライブラリを読み込む
import CaboCha

cabocha = CaboCha.Parser('-n1')

def parse_sentence(sentence_str, sentence_begin):
    # カボチャ関数の呼び出し、係り受け木を取得
    tree = cabocha.parse(sentence_str)

    offset = sentence_begin
    text = sentence_str

    for i in range(tree.chunk_size()):
        # chunk「文節に相当する塊」の事、chanking単語を一番小さい物に変換する
        chunk = tree.chunk(i)
        chunk_begin = None

        print('chunk:')

        #各チャンクの情報を取り出し。
        for j in range(
                chunk.token_pos,
                chunk.token_pos + chunk.token_size):
            # トークン（単語）とチャンクを切り分け表示する。
            token = tree.token(j)
            features = token.feature.split(',')
            # トークンの開始位置を指定
            token_begin = text.find(token.surface) + offset
            token_end = token_begin + len(token.surface)
            if chunk_begin is None:
                # チャンクの開始位置
                chunk_begin = token_begin

            print('    token_begin:', token_begin)
            print('    token_end:',   token_end)
            print('    features:',    features)
            print('    lemma:',       features[-3])
            print('    POS:',         features[0])
            print('    POS2:',        features[1])
            print('    NE:',          token.ne)
            print()

            text = text[token_end-offset:]
            # トークンの終了位置を指定
            offset = token_end
        # チャンクの終了位置
        chunk_end = token_end

        print('  chunk_link:',    chunk.link)
        print('  chunk_begin:',   chunk_begin)
        print('  chunk_end:',     chunk_end)
        print()


if __name__ == '__main__':
    parse_sentence('プログラムを作って、動かしながら自然言語処理を学ぶ事で、どんどん身につく', 0)
