from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime


class KnowledgeTagBase(SQLModel):
    """知识标签基础模型"""
    name: str


class KnowledgeTagCreate(KnowledgeTagBase):
    """创建知识标签模型"""
    pass


class KnowledgeTagInDB(KnowledgeTagBase):
    """数据库中的知识标签模型"""
    id: int
    usage_count: int
    created_at: datetime


class KnowledgeTag(KnowledgeTagInDB):
    """知识标签响应模型"""
    pass


class KnowledgeCategoryBase(SQLModel):
    """知识分类基础模型"""
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class KnowledgeCategoryCreate(KnowledgeCategoryBase):
    """创建知识分类模型"""
    pass


class KnowledgeCategoryUpdate(SQLModel):
    """更新知识分类模型"""
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None


class KnowledgeCategoryInDB(KnowledgeCategoryBase):
    """数据库中的知识分类模型"""
    id: int
    created_at: datetime
    updated_at: datetime


class KnowledgeCategory(KnowledgeCategoryInDB):
    """知识分类响应模型"""
    pass


class KnowledgeArticleBase(SQLModel):
    """知识文章基础模型"""
    title: str
    content: str
    summary: Optional[str] = None
    tags: Optional[str] = None
    category_id: Optional[int] = None
    status: str = "draft"


class KnowledgeArticleCreate(KnowledgeArticleBase):
    """创建知识文章模型"""
    pass


class KnowledgeArticleUpdate(SQLModel):
    """更新知识文章模型"""
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[str] = None


class KnowledgeArticleInDB(KnowledgeArticleBase):
    """数据库中的知识文章模型"""
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None


class KnowledgeArticle(KnowledgeArticleInDB):
    """知识文章响应模型"""
    pass
