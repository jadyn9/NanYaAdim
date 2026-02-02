from sqlmodel import SQLModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 创建同步引擎
engine = create_engine(
    "sqlite:///app.db",
    echo=settings.DEBUG,
    future=True
)

# 创建会话工厂
SessionLocal = sessionmaker(
    engine,
    expire_on_commit=False
)

def get_db():
    """
    获取数据库会话
    
    Yields:
        数据库会话实例
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    初始化数据库，创建所有表
    """
    # 创建所有表
    SQLModel.metadata.create_all(engine)
