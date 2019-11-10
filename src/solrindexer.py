import json
import urllib.parse
import urllib.request

# 使用するSolrのURL
solr_url = 'http://localhost:8983/solr'
# build_openerはログインが必要なサイトのときに使用する
opener = urllib.request.build_opener(urllib.request.ProxyHandler())

# Solrにデータを登録する関数、引数dataは登録するdataをdictで指定
def load(collection, data):
    
    # Solrのコアに対してデータを登録するリクエストを作成,collectionにはデータ登録先のコア名を指定している
    url='{0}/{1}/update'.format(solr_url, collection)
    # Requestインスタンスの作成,
    req = urllib.request.Request(
        url,
        # dataをdumps()でutf-8にエンコード
        data=json.dumps(data).encode('utf-8'),
        headers={'content-type': 'application/json'})

    # データの登録を実行
    print(url)
    # resでリクエストの返答を受け取る
    with opener.open(req) as res:
        # データ確認
        print(res.read().decode('utf-8'))

    # Solrのコアに対してコミット指示するリクエストを作成,collectionにはデータ登録先のコア名を指定している
    url = '{0}/{1}/update?softCommit=true'.format(solr_url, collection)
    # urlに対してリクエスト
    req = urllib.request.Request(url)
    # resuでリクエストの返答を受け取る、opnerはプロキシ環境変数に設定している場合も動くようにする為
    with opener.open(req) as res:
        # データを確認
        print(res.read().decode('utf-8'))
        
# solrプログラムから検索を行う関数
def search(keywords, rows=100):
    # keywordsは2重のリストとなる。ためkeywordsをgroup、groupをkeywordに
    query = ' AND '.join([
        # 内側のリストは「OR検索したい語」のリスト
        '(' + ' OR '.join([f'content_txt_ja:"{keyword}"' for keyword in group])
        # 外側のリストは「AND検索したいグループ」のリスト
        + ')' for group in keywords
    ])
    # 検索クエリの作成content_txt_jaフィールドを検索するクエリを作成する。
    data = {
        'q':     query,
        'wt':    'json',
        'rows':  rows,
        'hl':    'on',
        'hl.fl': 'content_txt_ja',
    }
    # 検索リクエストの作成（＊１）
    req = urllib.request.Request(
        # Solrでの検索APIは/select
        url=f'{solr_url}/doc/select',
        # JSON形式のデータをdataとして指定
        data=urllib.parse.urlencode(data).encode('utf-8'),)
    # 検索リクエストの実行（＊２）
    with opener.open(req) as res:
        # UTF-8のバイト列からUnicode文字列からなるstr型に変換し、JSON形式の文字列とみなしてdict型に変換したものを返す
        return json.loads(res.read().decode('utf-8'))

# アノテーションを見つける関数
def search_annotation(fl_keyword_pairs, rows=100):
    # fl_keyword_pairsは2重のリストとなる。ためfl_keyword_pairsをgroup、groupをkeywordに
    query = ' AND '.join([
        # 内側のリストは「OR検索したい語」のリスト
        '(' + ' OR '.join([f'{fl}:"{keyword}"' for keyword in group])
        # 外側のリストは「AND検索したいグループ」のリスト
        + ')' for fl, keywords in fl_keyword_pairs
            for group in keywords
    ])
    # 検索クエリの作成content_txt_jaフィールドを検索するクエリを作成する。
    data = {
        'q':     query,
        'wt':    'json',
        'rows':  rows,
    }
    # 検索リクエストの作成（＊１）
    req = urllib.request.Request(
        # Solrでの検索APIは/select
        url=f'{solr_url}/anno/select',
        # JSON形式のデータをdataとして指定
        data=urllib.parse.urlencode(data).encode('utf-8'),)
    # 検索リクエストの実行（＊２）
    with opener.open(req) as res:
        # UTF-8のバイト列からUnicode文字列からなるstr型に変換し、JSON形式の文字列とみなしてdict型に変換したものを返す
        return json.loads(res.read().decode('utf-8'))