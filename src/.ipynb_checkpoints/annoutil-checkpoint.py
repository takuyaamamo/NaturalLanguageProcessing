# 文内の単語を取得するための関数を作成
def find_xs_in_y(xs, y):
    return [x for x in xs if y['begin'] <= x['begin'] and x['end'] <= y['end']]
'''
リスト内包表記
for x in xs:
    if y['begin'] <= x['begin'] and x['end'] <= y['end']:
        return x

xs変数に格納されているアノテーションのリストからyアノテーションの内側に存在するものだけを取り出す関数
'''