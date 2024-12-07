from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///database/data.sqlite', echo=True)
Session = sessionmaker(bind=engine)

class ChatHistory(Base):
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)

Base.metadata.create_all(engine)
print("データベースを初期化しました。")
