from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlmodel import select
from datetime import datetime
from app.core.database import get_db
from app.models.knowledge import KnowledgeArticle, KnowledgeCategory, KnowledgeTag
from app.schemas.knowledge import (
    KnowledgeArticle as KnowledgeArticleSchema,
    KnowledgeArticleCreate,
    KnowledgeArticleUpdate,
    KnowledgeCategory as KnowledgeCategorySchema,
    KnowledgeCategoryCreate,
    KnowledgeCategoryUpdate,
    KnowledgeTag as KnowledgeTagSchema,
    KnowledgeTagCreate
)
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


# 知识标签管理

@router.get("/tag", response_model=List[KnowledgeTagSchema])
def get_knowledge_tags(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[KnowledgeTagSchema]:
    """
    获取知识标签列表
    
    Args:
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        知识标签列表
    """
    result = db.execute(select(KnowledgeTag))
    tags = result.scalars().all()
    return tags


# 知识分类管理

@router.post("/category", response_model=KnowledgeCategorySchema)
def create_knowledge_category(
    category_in: KnowledgeCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> KnowledgeCategorySchema:
    """
    创建知识分类
    
    Args:
        category_in: 创建知识分类模型
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        创建的知识分类信息
    """
    # 检查父分类是否存在
    if category_in.parent_id:
        result = db.execute(select(KnowledgeCategory).where(KnowledgeCategory.id == category_in.parent_id))
        parent = result.scalars().first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent category not found"
            )
    
    # 创建知识分类
    db_category = KnowledgeCategory(
        name=category_in.name,
        description=category_in.description,
        parent_id=category_in.parent_id
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


@router.get("/category", response_model=List[KnowledgeCategorySchema])
def get_knowledge_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[KnowledgeCategorySchema]:
    """
    获取知识分类列表
    
    Args:
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        知识分类列表
    """
    result = db.execute(select(KnowledgeCategory))
    categories = result.scalars().all()
    return categories


@router.put("/category/{category_id}", response_model=KnowledgeCategorySchema)
def update_knowledge_category(
    category_id: int,
    category_in: KnowledgeCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> KnowledgeCategorySchema:
    """
    更新知识分类
    
    Args:
        category_id: 知识分类ID
        category_in: 更新知识分类模型
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        更新后的知识分类信息
    
    Raises:
        HTTPException: 如果知识分类不存在
    """
    result = db.execute(select(KnowledgeCategory).where(KnowledgeCategory.id == category_id))
    category = result.scalars().first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge category not found"
        )
    
    # 检查父分类是否存在
    if category_in.parent_id:
        result = db.execute(select(KnowledgeCategory).where(KnowledgeCategory.id == category_in.parent_id))
        parent = result.scalars().first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent category not found"
            )
    
    # 更新知识分类信息
    update_data = category_in.dict(exclude_unset=True)
    
    # 更新知识分类属性
    for key, value in update_data.items():
        setattr(category, key, value)
    
    db.commit()
    db.refresh(category)
    
    return category


@router.delete("/category/{category_id}")
def delete_knowledge_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    删除知识分类
    
    Args:
        category_id: 知识分类ID
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        删除成功消息
    
    Raises:
        HTTPException: 如果知识分类不存在或包含子分类
    """
    result = db.execute(select(KnowledgeCategory).where(KnowledgeCategory.id == category_id))
    category = result.scalars().first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge category not found"
        )
    
    # 检查是否有子分类
    result = db.execute(select(KnowledgeCategory).where(KnowledgeCategory.parent_id == category_id))
    children = result.scalars().all()
    if children:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category with children"
        )
    
    # 检查是否有关联的知识文章
    result = db.execute(select(KnowledgeArticle).where(KnowledgeArticle.category_id == category_id))
    articles = result.scalars().all()
    if articles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category with articles"
        )
    
    db.delete(category)
    db.commit()
    
    return {"message": "Knowledge category deleted successfully"}


# 知识文章管理

@router.post("", response_model=KnowledgeArticleSchema)
def create_knowledge_article(
    article_in: KnowledgeArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> KnowledgeArticleSchema:
    """
    创建知识文章
    
    Args:
        article_in: 创建知识文章模型
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        创建的知识文章信息
    
    Raises:
        HTTPException: 如果知识分类不存在
    """
    # 检查知识分类是否存在
    if article_in.category_id:
        result = db.execute(select(KnowledgeCategory).where(KnowledgeCategory.id == article_in.category_id))
        category = result.scalars().first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge category not found"
            )
    
    # 处理标签
    if article_in.tags:
        # 分割标签
        tags = [tag.strip() for tag in article_in.tags.split(",") if tag.strip()]
        # 更新标签使用次数
        for tag_name in tags:
            result = db.execute(select(KnowledgeTag).where(KnowledgeTag.name == tag_name))
            tag = result.scalars().first()
            if tag:
                tag.usage_count += 1
            else:
                # 创建新标签
                new_tag = KnowledgeTag(name=tag_name, usage_count=1)
                db.add(new_tag)
    
    # 创建知识文章
    db_article = KnowledgeArticle(
        title=article_in.title,
        content=article_in.content,
        summary=article_in.summary,
        tags=article_in.tags,
        category_id=article_in.category_id,
        status=article_in.status,
        created_by=current_user.id
    )
    
    # 如果状态为published，设置发布时间
    if article_in.status == "published":
        db_article.published_at = datetime.utcnow()
    
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    
    return db_article


@router.get("", response_model=List[KnowledgeArticleSchema])
def get_knowledge_articles(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    status: Optional[str] = None,
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[KnowledgeArticleSchema]:
    """
    获取知识文章列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的最大记录数
        category_id: 知识分类ID，用于筛选
        status: 文章状态，用于筛选
        search: 搜索关键词
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        知识文章列表
    """
    query = select(KnowledgeArticle)
    
    # 应用筛选条件
    if category_id:
        query = query.where(KnowledgeArticle.category_id == category_id)
    
    if status:
        query = query.where(KnowledgeArticle.status == status)
    
    if search:
        # 简单的标题和内容搜索
        query = query.where(
            (KnowledgeArticle.title.contains(search)) |
            (KnowledgeArticle.content.contains(search)) |
            (KnowledgeArticle.tags.contains(search))
        )
    
    result = db.execute(query.offset(skip).limit(limit))
    articles = result.scalars().all()
    return articles


@router.get("/{article_id}", response_model=KnowledgeArticleSchema)
def get_knowledge_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> KnowledgeArticleSchema:
    """
    获取单个知识文章详情
    
    Args:
        article_id: 知识文章ID
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        知识文章详情
    
    Raises:
        HTTPException: 如果知识文章不存在
    """
    result = db.execute(select(KnowledgeArticle).where(KnowledgeArticle.id == article_id))
    article = result.scalars().first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge article not found"
        )
    return article


@router.put("/{article_id}", response_model=KnowledgeArticleSchema)
def update_knowledge_article(
    article_id: int,
    article_in: KnowledgeArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> KnowledgeArticleSchema:
    """
    更新知识文章
    
    Args:
        article_id: 知识文章ID
        article_in: 更新知识文章模型
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        更新后的知识文章信息
    
    Raises:
        HTTPException: 如果知识文章不存在或知识分类不存在
    """
    result = db.execute(select(KnowledgeArticle).where(KnowledgeArticle.id == article_id))
    article = result.scalars().first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge article not found"
        )
    
    # 检查知识分类是否存在
    if article_in.category_id:
        result = db.execute(select(KnowledgeCategory).where(KnowledgeCategory.id == article_in.category_id))
        category = result.scalars().first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge category not found"
            )
    
    # 处理标签更新
    if article_in.tags is not None:
        # 减少旧标签使用次数
        if article.tags:
            old_tags = [tag.strip() for tag in article.tags.split(",") if tag.strip()]
            for tag_name in old_tags:
                result = db.execute(select(KnowledgeTag).where(KnowledgeTag.name == tag_name))
                tag = result.scalars().first()
                if tag and tag.usage_count > 0:
                    tag.usage_count -= 1
        
        # 增加新标签使用次数
        if article_in.tags:
            new_tags = [tag.strip() for tag in article_in.tags.split(",") if tag.strip()]
            for tag_name in new_tags:
                result = db.execute(select(KnowledgeTag).where(KnowledgeTag.name == tag_name))
                tag = result.scalars().first()
                if tag:
                    tag.usage_count += 1
                else:
                    # 创建新标签
                    new_tag = KnowledgeTag(name=tag_name, usage_count=1)
                    db.add(new_tag)
    
    # 处理状态更新
    if article_in.status is not None:
        if article_in.status == "published" and article.status != "published":
            # 从草稿变为已发布，设置发布时间
            article.published_at = datetime.utcnow()
        elif article_in.status == "draft" and article.status == "published":
            # 从已发布变为草稿，清除发布时间
            article.published_at = None
    
    # 更新知识文章信息
    update_data = article_in.dict(exclude_unset=True)
    
    # 更新知识文章属性
    for key, value in update_data.items():
        setattr(article, key, value)
    
    db.commit()
    db.refresh(article)
    
    return article


@router.put("/{article_id}/publish", response_model=KnowledgeArticleSchema)
def publish_knowledge_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> KnowledgeArticleSchema:
    """
    发布知识文章
    
    Args:
        article_id: 知识文章ID
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        发布后的知识文章信息
    
    Raises:
        HTTPException: 如果知识文章不存在
    """
    result = db.execute(select(KnowledgeArticle).where(KnowledgeArticle.id == article_id))
    article = result.scalars().first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge article not found"
        )
    
    # 更新状态为已发布
    article.status = "published"
    if not article.published_at:
        article.published_at = datetime.utcnow()
    
    db.commit()
    db.refresh(article)
    
    return article


@router.put("/{article_id}/unpublish", response_model=KnowledgeArticleSchema)
def unpublish_knowledge_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> KnowledgeArticleSchema:
    """
    下架知识文章
    
    Args:
        article_id: 知识文章ID
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        下架后的知识文章信息
    
    Raises:
        HTTPException: 如果知识文章不存在
    """
    result = db.execute(select(KnowledgeArticle).where(KnowledgeArticle.id == article_id))
    article = result.scalars().first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge article not found"
        )
    
    # 更新状态为草稿
    article.status = "draft"
    article.published_at = None
    
    db.commit()
    db.refresh(article)
    
    return article


@router.delete("/{article_id}")
def delete_knowledge_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    删除知识文章
    
    Args:
        article_id: 知识文章ID
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        删除成功消息
    
    Raises:
        HTTPException: 如果知识文章不存在
    """
    result = db.execute(select(KnowledgeArticle).where(KnowledgeArticle.id == article_id))
    article = result.scalars().first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge article not found"
        )
    
    # 减少标签使用次数
    if article.tags:
        tags = [tag.strip() for tag in article.tags.split(",") if tag.strip()]
        for tag_name in tags:
            result = db.execute(select(KnowledgeTag).where(KnowledgeTag.name == tag_name))
            tag = result.scalars().first()
            if tag and tag.usage_count > 0:
                tag.usage_count -= 1
    
    db.delete(article)
    db.commit()
    
    return {"message": "Knowledge article deleted successfully"}
