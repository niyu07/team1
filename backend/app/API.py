from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .database import SessionLocal, init_db, seed_data
from sqlalchemy.orm import Session
from .models import Item

from pydantic import BaseModel
import datetime

# ★ Pydanticのインポートとスキーマの定義を追加
from pydantic import BaseModel
import datetime


class ItemBase(BaseModel):
    name: str
    detail: str | None = None
    tag: str | None = None
    state: bool = False  # Boolean型はデフォルト値を持たせることが多い


# クライアントがPOSTするデータ（作成時）
class ItemCreate(ItemBase):
    pass


# クライアントに返すデータ（読み取り時）
class ItemRead(ItemBase):
    id: int
    # dateもStringまたはDateTimeとして返す
    date: str | None = None

    # SQLAlchemyモデルからデータを読み込む設定
    class Config:
        from_attributes = True


app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()  # テーブル作成
    db = SessionLocal()
    seed_data(db)  # 初期データ投入
    db.close()


def get_DB() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/hello")
async def hello():
    return {"message": "Hello, World!"}


# アイテムリストで指定することを想定し，ダミーのエンドポイントを作成
@app.get("/ItemList/getItem/")
async def get_item(db: Session = Depends(get_DB)):
    items = db.query(Item).all()
    return items


@app.post(
    "/api/createItem/", response_model=ItemRead
)  # ★ Pydanticモデルを受け取って返すように変更
async def create_item(
    item_data: ItemCreate,  # ★ Pydanticモデルでデータを受け取る
    db: Session = Depends(get_DB),  # ★ DBセッションの依存性を追加
):
    # PydanticモデルのデータをSQLAlchemyモデルにマッピング
    db_item = Item(
        name=item_data.name,
        detail=item_data.detail,
        tag=item_data.tag,
        state=item_data.state,
        # dateはmodels.pyでデフォルト値を設定しているため、ここでは渡さない
    )

    # データベースへの操作
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    # IDやdateが設定されたオブジェクトをPydanticモデル形式で返す
    return db_item
