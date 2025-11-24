from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .database import SessionLocal, init_db, seed_data
from sqlalchemy.orm import Session
from .models import Item

from fastapi import HTTPException

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


@app.post("/api/createItem/")
async def create_item(item: dict):
    return {"message": "Item created successfully.", "item": item}


# 多分いらんけど，一応確認用として
@app.get("/api/{id}/getItem")
async def get_item_by_id(id: int, db: Session = Depends(get_DB)):
    item_by_id = db.query(Item).filter(Item.id == id).first()
    if item_by_id is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_by_id


# タグ検索用
@app.get("/api/{tag}/getItems")
async def get_items_by_tag(tag: str, db: Session = Depends(get_DB)):
    items_by_tag = db.query(Item).filter(Item.tag == tag).all()
    if not items_by_tag:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_by_tag
