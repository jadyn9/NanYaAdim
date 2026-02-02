from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class KnowledgeTag(SQLModel, table=True):
    """知识标签模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., index=True, unique=True, description="标签名称")
    usage_count: int = Field(default=0, description="使用次数")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")


class KnowledgeCategory(SQLModel, table=True):
    """知识分类模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., index=True, description="分类名称")
    description: Optional[str] = Field(default=None, description="分类描述")
    parent_id: Optional[int] = Field(default=None, foreign_key="knowledgecategory.id", description="父分类ID")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")
    
    # 关系
    parent: Optional["KnowledgeCategory"] = Relationship(back_populates="children", sa_relationship_kwargs={"remote_side": "KnowledgeCategory.id"})
    children: List["KnowledgeCategory"] = Relationship(back_populates="parent")
    articles: List["KnowledgeArticle"] = Relationship(back_populates="category")


class KnowledgeArticle(SQLModel, table=True):
    """知识文章模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(..., index=True, description="文章标题")
    content: str = Field(..., description="文章内容")
    summary: Optional[str] = Field(default=None, description="文章摘要")
    tags: Optional[str] = Field(default=None, description="标签列表，逗号分隔")
    category_id: Optional[int] = Field(default=None, foreign_key="knowledgecategory.id", description="分类ID")
    status: str = Field(default="draft", description="状态(draft/published)")
    created_by: Optional[int] = Field(default=None, description="创建者ID")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")
    published_at: Optional[datetime] = Field(default=None, description="发布时间")
    
    # 关系
    category: Optional[KnowledgeCategory] = Relationship(back_populates="articles")
