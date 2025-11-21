from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .database import SessionLocal, init_db, seed_data
from .models import Item

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


def get_DB():
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
async def get_item(db: SessionLocal = Depends(get_DB)):
    items = db.query(Item).all()
    return items


@app.post("/api/createItem/")
async def create_item(item: dict):
    return {"message": "Item created successfully.", "item": item}
