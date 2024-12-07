# config.py

class Config:
    # モデル設定
    vocab_size = 1000
    embed_size = 128
    hidden_size = 256

    # データベース設定
    db_url = 'sqlite:///database/data.sqlite'
    knowledge_db_url = 'sqlite:///database/knowledge_base.db'
