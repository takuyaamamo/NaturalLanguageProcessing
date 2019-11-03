import json
import urllib.parse
import urllib.request

# 使用するSolrのURL
solr_url = 'http://localhost:8983/solr'
# build_openerはログインが必要なサイトのときに使用する
opener = urllib.request.build_opener(urllib.request.ProxyHandler())

# Solrにデータを登録する関数、引数dataは登録するdataをdictで指定
def solr_load(collection, data):
    
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