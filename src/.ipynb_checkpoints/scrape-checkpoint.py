# 正規表現を行うライブラリ
import re
# ユニコードの正規化を行うライブラリ
import unicodedata
from bs4 import BeautifulSoup

# maketransでdictで指定した変換法則をtranslation_tableにセットする
translation_table = str.maketrans(dict(zip('()!', '（）！')))

# クレンジング関数を定義
def cleanse(text):
    # NFKCというユニコードの五感文字に変換を行う。更にtranslation_tableを行う。
    text = unicodedata.normalize('NFKC', text).translate(translation_table)
    # 第2引数の文字列を第1引数に変換
    text = re.sub(r'\s+', ' ', text)
    return text

# スクレイピング関数を定義
def scrape(html):
    soup = BeautifulSoup(html, 'html.parser')
    # __EOS__ の挿入
    # BeautifulSoupのfind_allでタグを検索し取り出している
    for block in soup.find_all(['br', 'p', 'h1', 'h2', 'h3', 'h4']):
        if len(block.text.strip()) > 0 and block.text.strip()[-1] not in ['。', '！']:
            block.append('<__EOS__>')
    # 本文の抽出
    text = '\n'.join([cleanse(block.text.strip())
                      for block in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4'])
                      if len(block.text.strip()) > 0])
    # タイトルの抽出
    title = cleanse(soup.title.text.replace(' - Wikipedia', ''))
    return text, title
