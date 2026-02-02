from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class Role(SQLModel, table=True):
    """角色模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., index=True, unique=True, description="角色名称")
    description: Optional[str] = Field(default=None, description="角色描述")
    permissions: Optional[str] = Field(default=None, description="权限列表")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    
    # 关系
    users: List["User"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    """用户模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(..., index=True, unique=True, description="用户名")
    password: str = Field(..., description="密码哈希")
    name: str = Field(..., description="姓名")
    email: str = Field(..., index=True, unique=True, description="邮箱")
    role_id: Optional[int] = Field(default=None, foreign_key="role.id", description="角色ID")
    status: bool = Field(default=True, description="状态")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")
    
    # 关系
    role: Optional[Role] = Relationship(back_populates="users")
