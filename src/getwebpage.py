import urllib.request
# 文字コードの変換: 自動で文字コードを判定する
import cchardet
# HTML構造を解析し、タグ名やタグの属性で指定した部分のみを取り出すことができる
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # 日本のウィキペディアページを指定
    url = 'https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC'
    with urllib.request.urlopen(url) as res:
        byte = res.read()
        # 文字コードの変換
        html = byte.decode(cchardet.detect(byte)['encoding'])
        # BeautifulSoupの読み出し
        soup = BeautifulSoup(html, 'html.parser')
        # <title>タグ内のテキストを抜き出し
        title = soup.head.title
        print('[title]:', title.text, '\n')

        # p,h1,h2,h3,h4の内容を抜き出し
        for block in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4']):
            print('[block]:', block.text)
