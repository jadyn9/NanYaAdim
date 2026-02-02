from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class ArchiveCategory(SQLModel, table=True):
    """档案分类模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., index=True, description="分类名称")
    description: Optional[str] = Field(default=None, description="分类描述")
    parent_id: Optional[int] = Field(default=None, foreign_key="archivecategory.id", description="父分类ID")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")
    
    # 关系
    parent: Optional["ArchiveCategory"] = Relationship(back_populates="children", sa_relationship_kwargs={"remote_side": "ArchiveCategory.id"})
    children: List["ArchiveCategory"] = Relationship(back_populates="parent")
    archives: List["Archive"] = Relationship(back_populates="category")


class Archive(SQLModel, table=True):
    """档案模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(..., index=True, description="档案标题")
    description: Optional[str] = Field(default=None, description="档案描述")
    file_path: Optional[str] = Field(default=None, description="文件路径")
    category_id: Optional[int] = Field(default=None, foreign_key="archivecategory.id", description="分类ID")
    archive_type: str = Field(default="document", description="档案类型")
    created_by: Optional[int] = Field(default=None, description="创建者ID")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")
    
    # 关系
    category: Optional[ArchiveCategory] = Relationship(back_populates="archives")
