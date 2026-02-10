from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import select
from app.core.database import get_db
from app.models.archive import Archive, ArchiveCategory
from app.schemas.archive import (
    Archive as ArchiveSchema,
    ArchiveCreate,
    ArchiveUpdate,
    ArchiveCategory as ArchiveCategorySchema,
    ArchiveCategoryCreate,
    ArchiveCategoryUpdate
)
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/api/archive", tags=["archive"])


# 档案分类管理

@router.post("/category", response_model=ArchiveCategorySchema)
def create_archive_category(
    category_in: ArchiveCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> ArchiveCategorySchema:
    """
    创建档案分类
    
    Args:
        category_in: 创建档案分类模型
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        创建的档案分类信息
    """
    # 检查父分类是否存在
    if category_in.parent_id:
        result = db.execute(select(ArchiveCategory).where(ArchiveCategory.id == category_in.parent_id))
        parent = result.scalars().first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent category not found"
            )
    
    # 创建档案分类
    db_category = ArchiveCategory(
        name=category_in.name,
        description=category_in.description,
        parent_id=category_in.parent_id
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


@router.get("/category", response_model=List[ArchiveCategorySchema])
def get_archive_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[ArchiveCategorySchema]:
    """
    获取档案分类列表
    
    Args:
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        档案分类列表
    """
    result = db.execute(select(ArchiveCategory))
    categories = result.scalars().all()
    return categories


@router.put("/category/{category_id}", response_model=ArchiveCategorySchema)
def update_archive_category(
    category_id: int,
    category_in: ArchiveCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> ArchiveCategorySchema:
    """
    更新档案分类
    
    Args:
        category_id: 档案分类ID
        category_in: 更新档案分类模型
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        更新后的档案分类信息
    
    Raises:
        HTTPException: 如果档案分类不存在
    """
    result = db.execute(select(ArchiveCategory).where(ArchiveCategory.id == category_id))
    category = result.scalars().first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archive category not found"
        )
    
    # 检查父分类是否存在
    if category_in.parent_id:
        result = db.execute(select(ArchiveCategory).where(ArchiveCategory.id == category_in.parent_id))
        parent = result.scalars().first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent category not found"
            )
    
    # 更新档案分类信息
    update_data = category_in.dict(exclude_unset=True)
    
    # 更新档案分类属性
    for key, value in update_data.items():
        setattr(category, key, value)
    
    db.commit()
    db.refresh(category)
    
    return category


@router.delete("/category/{category_id}")
def delete_archive_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    删除档案分类
    
    Args:
        category_id: 档案分类ID
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        删除成功消息
    
    Raises:
        HTTPException: 如果档案分类不存在或包含子分类
    """
    result = db.execute(select(ArchiveCategory).where(ArchiveCategory.id == category_id))
    category = result.scalars().first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archive category not found"
        )
    
    # 检查是否有子分类
    result = db.execute(select(ArchiveCategory).where(ArchiveCategory.parent_id == category_id))
    children = result.scalars().all()
    if children:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category with children"
        )
    
    # 检查是否有关联的档案
    result = db.execute(select(Archive).where(Archive.category_id == category_id))
    archives = result.scalars().all()
    if archives:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category with archives"
        )
    
    db.delete(category)
    db.commit()
    
    return {"message": "Archive category deleted successfully"}


# 档案管理

@router.post("", response_model=ArchiveSchema)
def create_archive(
    archive_in: ArchiveCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> ArchiveSchema:
    """
    创建新档案
    
    Args:
        archive_in: 创建档案模型
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        创建的档案信息
    
    Raises:
        HTTPException: 如果档案分类不存在
    """
    # 检查档案分类是否存在
    if archive_in.category_id:
        result = db.execute(select(ArchiveCategory).where(ArchiveCategory.id == archive_in.category_id))
        category = result.scalars().first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Archive category not found"
            )
    
    # 创建档案
    db_archive = Archive(
        title=archive_in.title,
        description=archive_in.description,
        file_path=archive_in.file_path,
        category_id=archive_in.category_id,
        archive_type=archive_in.archive_type,
        created_by=current_user.id
    )
    
    db.add(db_archive)
    db.commit()
    db.refresh(db_archive)
    
    return db_archive


@router.get("", response_model=List[ArchiveSchema])
def get_archives(
    page: int = 1,
    page_size: int = 10,
    name: str = None,
    category_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[ArchiveSchema]:
    """
    获取档案列表
    
    Args:
        page: 页码，从1开始
        page_size: 每页记录数
        name: 档案名称，用于筛选
        category_id: 档案分类ID，用于筛选
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        档案列表
    """
    # 计算跳过的记录数
    skip = (page - 1) * page_size
    limit = page_size
    
    query = select(Archive)
    
    # 如果指定了分类，筛选该分类下的档案
    if category_id:
        query = query.where(Archive.category_id == category_id)
    
    # 如果指定了名称，筛选包含该名称的档案
    if name:
        query = query.where(Archive.title.contains(name))
    
    result = db.execute(query.offset(skip).limit(limit))
    archives = result.scalars().all()
    return archives


@router.get("/{archive_id}", response_model=ArchiveSchema)
def get_archive(
    archive_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> ArchiveSchema:
    """
    获取单个档案详情
    
    Args:
        archive_id: 档案ID
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        档案详情
    
    Raises:
        HTTPException: 如果档案不存在
    """
    result = db.execute(select(Archive).where(Archive.id == archive_id))
    archive = result.scalars().first()
    if not archive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archive not found"
        )
    return archive


@router.put("/{archive_id}", response_model=ArchiveSchema)
def update_archive(
    archive_id: int,
    archive_in: ArchiveUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> ArchiveSchema:
    """
    更新档案信息
    
    Args:
        archive_id: 档案ID
        archive_in: 更新档案模型
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        更新后的档案信息
    
    Raises:
        HTTPException: 如果档案不存在或档案分类不存在
    """
    result = db.execute(select(Archive).where(Archive.id == archive_id))
    archive = result.scalars().first()
    if not archive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archive not found"
        )
    
    # 检查档案分类是否存在
    if archive_in.category_id:
        result = db.execute(select(ArchiveCategory).where(ArchiveCategory.id == archive_in.category_id))
        category = result.scalars().first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Archive category not found"
            )
    
    # 更新档案信息
    update_data = archive_in.dict(exclude_unset=True)
    
    # 更新档案属性
    for key, value in update_data.items():
        setattr(archive, key, value)
    
    db.commit()
    db.refresh(archive)
    
    return archive


@router.delete("/{archive_id}")
def delete_archive(
    archive_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    删除档案
    
    Args:
        archive_id: 档案ID
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        删除成功消息
    
    Raises:
        HTTPException: 如果档案不存在
    """
    result = db.execute(select(Archive).where(Archive.id == archive_id))
    archive = result.scalars().first()
    if not archive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archive not found"
        )
    
    db.delete(archive)
    db.commit()
    
    return {"message": "Archive deleted successfully"}
