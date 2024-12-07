# database/knowledge_base.py

import requests
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

# SQLiteデータベースの準備
engine = create_engine("sqlite:///database/knowledge_base.db")
metadata = MetaData()

# 専門知識テーブルの作成
knowledge_table = Table(
    'knowledge',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('category', String),
    Column('source', String),
    Column('content', String)
)
metadata.create_all(engine)

# PubMedデータセット取得モジュール
def fetch_pubmed(query, max_results=10):
    """PubMedからデータを取得"""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmax={max_results}&retmode=json"
    response = requests.get(url)
    ids = response.json().get('esearchresult', {}).get('idlist', [])
    
    fetched_data = []
    for pub_id in ids:
        detail_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pub_id}&retmode=json"
        detail_resp = requests.get(detail_url)
        summary = detail_resp.json().get('result', {}).get(pub_id, {}).get('title', 'No Title')
        fetched_data.append({"id": pub_id, "content": summary})
    return fetched_data

# データベースに保存
def save_to_db(data, category):
    conn = engine.connect()
    for entry in data:
        conn.execute(knowledge_table.insert(), {
            "category": category,
            "source": "PubMed",
            "content": entry['content']
        })

# データベースからデータを取得
def get_knowledge_by_category(category):
    conn = engine.connect()
    result = conn.execute(knowledge_table.select().where(knowledge_table.c.category == category))
    return [{"id": row["id"], "category": row["category"], "source": row["source"], "content": row["content"]} for row in result]
