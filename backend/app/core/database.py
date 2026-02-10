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
    初始化数据库，创建所有表并添加默认角色和用户
    """
    # 创建所有表
    SQLModel.metadata.create_all(engine)
    
    # 添加默认角色和用户
    from app.models.user import User, Role
    from app.core.security import get_password_hash
    
    db = SessionLocal()
    try:
        # 检查是否已有admin用户
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            # 检查是否已有admin角色
            admin_role = db.query(Role).filter(Role.name == "admin").first()
            if not admin_role:
                # 创建admin角色
                admin_role = Role(name="admin", description="管理员")
                db.add(admin_role)
                db.commit()
                db.refresh(admin_role)
            
            # 确保密码长度不超过72字节
            password = "admin123"
            if len(password) > 72:
                password = password[:72]
            
            # 创建默认管理员用户
            admin_user = User(
                username="admin",
                password=get_password_hash(password),
                name="管理员",
                email="admin@example.com",
                role_id=admin_role.id,
                status=True
            )
            db.add(admin_user)
            db.commit()
            print("默认管理员用户创建成功")
    except Exception as e:
        print(f"初始化默认数据时出错: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()
