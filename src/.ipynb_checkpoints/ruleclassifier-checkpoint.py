# 有名がある時Trueを返す。
def contain_yumei(tokens):
    for token in tokens:
        if token['lemma'] == '有名':
            return True
    return False

# 地名を含んでいる時Trueを返す
def contain_LOC(tokens):
    for token in tokens:
        # getメソッドは、第一引数の'NE'がdictにあれば値を返し、なければデフォルトでNone、指定されていれば第2引数の値を返す。
        # endswithメソッドは、文字列が指定した引数の検索する文字列で終わっていればtrueを返し、そうでない場合はfalseを返す。
        if token.get('NE', '').endswith('LOCATION'):
            return True
    return False

# おいしいがある時Trueを返す。
def contain_oishii(tokens):
    for token in tokens:
        if token['lemma'] == 'おいしい':
            return True
    return False

# 上記3つのルールを組み合わせて分析結果を簡単に返す
def meibutsu_rule(feature):
    # 有名と地名が両方ある時
    if feature['contain_yumei'] and feature['contain_LOC']:
        return 1
    # 美味しいがある時
    if feature['contain_oishii']:
        return 1
    return 0

# 個別ルールと最終的な分類結果を判定するルールを返す関数
def get_rule():
    return {
        'partial': {
            'contain_yumei': contain_yumei,
            'contain_LOC': contain_LOC,
            'contain_oishii': contain_oishii,
        },
        'compound': meibutsu_rule
    }

# 引数で渡されたルールを文に適応させる
def convert_into_features_using_rules(sentences, rule):
    features = []
    for doc_id, sent, tokens in sentences:
        feature = {}
        # items()でdictのkeyとvalue両方を取り出す
        for name, func in rule['partial'].items():
            feature[name] = func(tokens)
        features.append(feature)
    return features

# 引数で渡された分類ルールを適応し、分類結果を返す
def classify(features, rule):
    return [rule['compound'](feature) for feature in features]