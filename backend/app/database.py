from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # とりあえずSQLiteでOK

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ★★★ 超重要：テーブルを自動作成する ★★★
def init_db():
    from . import models
    Base.metadata.create_all(bind=engine)

def seed_data(db):
    from .models import Item

    # 既にデータがあればスキップ
    if db.query(Item).first():
        return

    # 初期データ
    items = [
        Item(name="りんご"),
        Item(name="バナナ"),
        Item(name="みかん"),
    ]

    db.add_all(items)
    db.commit()
