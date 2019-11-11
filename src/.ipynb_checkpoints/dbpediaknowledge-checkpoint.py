from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from SPARQLWrapper import JSON, SPARQLWrapper

import cabochaparser as parser

def get_synonyms(text):
    # 同義語を取得したい語の文字列をuriに代入
    uri = f'<http://ja.dbpedia.org/resource/{text}>'
    
    # 公開されているSPARQLエンドポイントを指定、ここからDBpediaを使用することができる
    sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')
    # 戻り値をJSONフォーマットに指定
    sparql.setReturnFormat(JSON)
    # format関数では{}がエスケープされる為2重に繰り返して{{}}とする必要がある。
    # UNIONでつなげる事で同義語展開ができる。最後にURIをラベルに変換したものをsynonym変数に格納する。
    # Wikipediaの記事タイトルをsynonym変数として取得される。
    sparql.setQuery(f'''
        SELECT DISTINCT *
        WHERE {{
                {{ ?redirect <http://dbpedia.org/ontology/wikiPageRedirects> {uri} }}
                UNION
                {{ {uri} <http://dbpedia.org/ontology/wikiPageRedirects> ?redirect }} .
                ?redirect <http://www.w3.org/2000/01/rdf-schema#label> ?synonym
                }}
    ''')
    
    results = []
    for x in sparql.query().convert()['results']['bindings']:
        word = x['synonym']['value']
        results.append({'term': word})
    return results

def retrieve_abstract(text):
    uri = f'<http://ja.dbpedia.org/resource/{text}>'
    
    sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')
    sparql.setReturnFormat(JSON)
    # 主語に指定された記事を、術語にアブストラクトのURIを指定し、目的語として帰ってくるものをsummary変数で受け取っている。
    sparql.setQuery(f'''
        SELECT DISTINCT *
        WHERE {{
            {uri} <http://dbpedia.org/ontology/abstract> ?summary
        }}
    ''')
    results = sparql.query().convert()['results']['bindings']
    if len(results) > 0:
        return results[0]['summary']['value']
    else:
        return None
    
# 類似度の計算
def calc_similarity(text1, text2, vectorizer=None):
    # textそれぞれについてのtokenをとりだし、docいまとめる。
    summary1 = retrieve_abstract(text1)
    summary2 = retrieve_abstract(text2)
    if summary1 is None or summary2 is None:
        return 0.
    sentences1, chunks1, tokens1 = parser.parse(summary1)
    doc1 = ''.join([token['lemma'] for token in tokens1])
    sentences2, chunks2, tokens2 = parser.parse(summary2)
    doc2 = ''.join([token['lemma'] for token in tokens2])
    
    vectorizer = CountVectorizer(analyzer='word')
    vecs = vectorizer.fit_transform([doc1, doc2])
    
    # コサイン類似度で比べる
    sim = cosine_similarity(vecs)
    
    return sim[0][1]

def get_population(text):
    uri = f'<http://ja.dbpedia.org/resource/{text}>'
    
    # 述語に人工値を表すURIを指定し、取得した値をpopulation変数で受け取る。
    sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')
    sparql.setReturnFormat(JSON)
    sparql.setQuery(f'''
        SELECT DISTINCT *
        WHERE {{
            {uri} <http://ja.dbpedia.org/property/人口値> ?population
        }}
    ''')

    results = sparql.query().convert()['results']['bindings']
    # データが見つからない場合は-1を返す
    if len(results) > 0:
        population = results[0]['population']['value']
        return int(population)
    else:
        return -1
