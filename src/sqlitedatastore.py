import json
import sqlite3

conn = None

# データベース接続
def connect():
    # global変数でconnを呼び出し
    global conn
    # データベースの場所を指定
    conn = sqlite3.connect('../data/sqlite3/sqlite3')

# データベース接続終了
def close():
    # 終了
    conn.close()

# テーブル作成
def create_table():
    # executeでSQL構文作成、docsがあれば削除
    conn.execute('DROP TABLE IF EXISTS docs')
    # docsテーブルを新規作成
    conn.execute('''CREATE TABLE docs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            content     TEXT,
            meta_info   BLOB,
            sentence    BLOB,
            chunk       BLOB,
            token       BLOB
        )''')

# データをインサートする
def load(values):
    # exucutemany()はvaluesに指定したパラメータ順序またはマッピングを?に入れて実行できる
    conn.executemany('INSERT INTO docs (content, meta_info) VALUES (?,?)', values)
    # 確定
    conn.commit()

# 一部のデータを見る
def get(doc_id, fl):
    #.fetchone()で指定した1行を取得
    row_ls = conn.execute(f"SELECT {','.join(fl)} FROM docs WHERE id = {doc_id}").fetchone()
    # row_ls = conn.execute('SELECT {} FROM docs WHERE id = ?'.format(','.join(fl)),(doc_id,)).fetchone()
    row_dict = {}
    # flとrow_lsで抜き出したデータをzipする
    for key, value in zip(fl, row_ls):
        row_dict[key] = value
    return row_dict

# id番号を抜き出す
def get_all_ids(limit, offset=0):
    return [record[0] for record in
            # limitで取得上限、OFFSETで開始位置を指定してデータを抜き出す。そのデータの1番目id番号を抜き出す
            conn.execute(f'SELECT id FROM docs LIMIT {limit} OFFSET {offset}')]
            # conn.execute('SELECT id FROM docs LIMIT ? OFFSET ?',(limit, offset))]

def set_annotation(doc_id, name, value):
    conn.execute(
        'UPDATE docs SET {0} = ? where id = ?'.format(name),
        (json.dumps(value), doc_id))
    conn.commit()

# アノテーションを取得
def get_annotation(doc_id, name):
    # docsのid行をwhere idで指定しnameから取り出す
    row = conn.execute(f'SELECT {name} FROM docs WHERE id = {doc_id}').fetchone()
    if row[0] is not None:
        return json.loads(row[0])
    else:
        return []
