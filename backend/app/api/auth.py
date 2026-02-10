from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlmodel import select
from app.core.config import settings
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User, Role
from app.schemas.user import Token, User as UserSchema, UserCreate
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Token:
    """
    用户登录
    
    Args:
        form_data: OAuth2密码请求表单
        db: 数据库会话
    
    Returns:
        包含访问令牌的响应
    
    Raises:
        HTTPException: 如果用户名或密码错误
    """
    # 暂时使用硬编码的方式验证用户名和密码
    if form_data.username != "admin" or form_data.password != "admin123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "admin", "id": 1},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    用户登出
    
    Args:
        current_user: 当前活跃用户
    
    Returns:
        登出成功消息
    """
    # JWT是无状态的，登出只需客户端删除令牌即可
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserSchema)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
) -> UserSchema:
    """
    获取当前用户信息
    
    Args:
        current_user: 当前活跃用户
    
    Returns:
        当前用户信息
    """
    return current_user


@router.post("/register", response_model=UserSchema)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
) -> UserSchema:
    """
    用户注册
    
    Args:
        user_in: 创建用户模型
        db: 数据库会话
    
    Returns:
        创建的用户信息
    
    Raises:
        HTTPException: 如果用户名或邮箱已存在
    """
    # 检查用户名是否已存在
    result = db.execute(select(User).where(User.username == user_in.username))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # 检查邮箱是否已存在
    result = db.execute(select(User).where(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 创建用户
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        password=hashed_password,
        name=user_in.name,
        email=user_in.email,
        role_id=user_in.role_id
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
