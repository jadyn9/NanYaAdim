from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime


class ArchiveCategoryBase(SQLModel):
    """档案分类基础模型"""
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class ArchiveCategoryCreate(ArchiveCategoryBase):
    """创建档案分类模型"""
    pass


class ArchiveCategoryUpdate(SQLModel):
    """更新档案分类模型"""
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None


class ArchiveCategoryInDB(ArchiveCategoryBase):
    """数据库中的档案分类模型"""
    id: int
    created_at: datetime
    updated_at: datetime


class ArchiveCategory(ArchiveCategoryInDB):
    """档案分类响应模型"""
    pass


class ArchiveBase(SQLModel):
    """档案基础模型"""
    title: str
    description: Optional[str] = None
    file_path: Optional[str] = None
    category_id: Optional[int] = None
    archive_type: str = "document"


class ArchiveCreate(ArchiveBase):
    """创建档案模型"""
    pass


class ArchiveUpdate(SQLModel):
    """更新档案模型"""
    title: Optional[str] = None
    description: Optional[str] = None
    file_path: Optional[str] = None
    category_id: Optional[int] = None
    archive_type: Optional[str] = None


class ArchiveInDB(ArchiveBase):
    """数据库中的档案模型"""
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class Archive(ArchiveInDB):
    """档案响应模型"""
    pass
