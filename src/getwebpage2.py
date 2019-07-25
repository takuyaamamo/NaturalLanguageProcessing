import urllib.request
# 文字コードの変換: 自動で文字コードを判定する
import cchardet

# src/scrape.py をライブラリとしてインポート
import scrape

if __name__ == '__main__':
    # 日本のウィキペディアページを指定
    url = 'https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC'
    with urllib.request.urlopen(url) as res:
        byte = res.read()
        # 文字コードの変換
        html = byte.decode(cchardet.detect(byte)['encoding'])
        # scrape関数によりスクレイピングとクレンジングを行う
        text, title = scrape.scrape(html)
        print('[title]: ', title)
        print('[text]:  ', text[:1000])
