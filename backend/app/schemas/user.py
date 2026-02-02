from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime


class UserBase(SQLModel):
    """用户基础模型"""
    username: str
    name: str
    email: str
    role_id: Optional[int] = None


class UserCreate(UserBase):
    """创建用户模型"""
    password: str


class UserUpdate(SQLModel):
    """更新用户模型"""
    name: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[int] = None
    password: Optional[str] = None
    status: Optional[bool] = None


class UserInDB(UserBase):
    """数据库中的用户模型"""
    id: int
    status: bool
    created_at: datetime
    updated_at: datetime


class User(UserInDB):
    """用户响应模型"""
    pass


class UserLogin(SQLModel):
    """用户登录模型"""
    username: str
    password: str


class Token(SQLModel):
    """令牌模型"""
    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    """令牌数据模型"""
    username: Optional[str] = None
    user_id: Optional[int] = None


class RoleBase(SQLModel):
    """角色基础模型"""
    name: str
    description: Optional[str] = None
    permissions: Optional[str] = None


class RoleCreate(RoleBase):
    """创建角色模型"""
    pass


class RoleUpdate(SQLModel):
    """更新角色模型"""
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[str] = None


class RoleInDB(RoleBase):
    """数据库中的角色模型"""
    id: int
    created_at: datetime


class Role(RoleInDB):
    """角色响应模型"""
    pass
