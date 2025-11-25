from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # とりあえずSQLiteでOK

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ★★★ 超重要：テーブルを自動作成する ★★★
def init_db():
    from . import models

    _ = models
    Base.metadata.create_all(bind=engine)


def seed_data(db):
    from .models import Item

    # 既にデータがあればスキップ
    if db.query(Item).first():
        return

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 初期データ
    items = [
        Item(
            name="りんご",
            date="2025-11-20 10:00:00",
            detail="駅前のスーパーが安い",
            tag="果物",
            state=True,
        ),
        Item(
            name="バナナ",
            # dateを省略すると、models.pyで設定したデフォルト値（現在時刻の文字列）が入る
            detail="駅前のスーパーが安い",
            tag="果物",
            state=True,
        ),
        Item(
            name="みかん",
            # 変数を使って現在の時刻の文字列を渡すこともできる
            date=now_str,
            detail="駅前のスーパーが安い",
            tag="果物",
            state=True,
        ),
    ]

    db.add_all(items)
    db.commit()
