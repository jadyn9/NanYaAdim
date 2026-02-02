from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import select
from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.user import User, Role
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate, Role as RoleSchema, RoleCreate, RoleUpdate
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("", response_model=UserSchema)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> UserSchema:
    """
    创建新用户
    
    Args:
        user_in: 创建用户模型
        db: 数据库会话
        current_user: 当前活跃用户
    
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
            detail="Username already exists"
        )
    
    # 检查邮箱是否已存在
    result = db.execute(select(User).where(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
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


@router.get("", response_model=List[UserSchema])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[UserSchema]:
    """
    获取用户列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的最大记录数
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        用户列表
    """
    result = db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users


@router.get("/{user_id}", response_model=UserSchema)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> UserSchema:
    """
    获取单个用户信息
    
    Args:
        user_id: 用户ID
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        用户信息
    
    Raises:
        HTTPException: 如果用户不存在
    """
    result = db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> UserSchema:
    """
    更新用户信息
    
    Args:
        user_id: 用户ID
        user_in: 更新用户模型
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        更新后的用户信息
    
    Raises:
        HTTPException: 如果用户不存在
    """
    result = db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # 更新用户信息
    update_data = user_in.dict(exclude_unset=True)
    
    # 如果更新密码，需要哈希处理
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
    
    # 更新用户属性
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    删除用户
    
    Args:
        user_id: 用户ID
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        删除成功消息
    
    Raises:
        HTTPException: 如果用户不存在
    """
    result = db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}


# 角色管理接口

@router.post("/roles", response_model=RoleSchema)
def create_role(
    role_in: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> RoleSchema:
    """
    创建新角色
    
    Args:
        role_in: 创建角色模型
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        创建的角色信息
    
    Raises:
        HTTPException: 如果角色名称已存在
    """
    # 检查角色名称是否已存在
    result = db.execute(select(Role).where(Role.name == role_in.name))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role name already exists"
        )
    
    # 创建角色
    db_role = Role(
        name=role_in.name,
        description=role_in.description,
        permissions=role_in.permissions
    )
    
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    
    return db_role


@router.get("/roles", response_model=List[RoleSchema])
def get_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[RoleSchema]:
    """
    获取角色列表
    
    Args:
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        角色列表
    """
    result = db.execute(select(Role))
    roles = result.scalars().all()
    return roles


@router.put("/roles/{role_id}", response_model=RoleSchema)
def update_role(
    role_id: int,
    role_in: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> RoleSchema:
    """
    更新角色信息
    
    Args:
        role_id: 角色ID
        role_in: 更新角色模型
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        更新后的角色信息
    
    Raises:
        HTTPException: 如果角色不存在
    """
    result = db.execute(select(Role).where(Role.id == role_id))
    role = result.scalars().first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    # 更新角色信息
    update_data = role_in.dict(exclude_unset=True)
    
    # 更新角色属性
    for key, value in update_data.items():
        setattr(role, key, value)
    
    db.commit()
    db.refresh(role)
    
    return role


@router.delete("/roles/{role_id}")
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    删除角色
    
    Args:
        role_id: 角色ID
        db: 数据库会话
        current_user: 当前活跃用户
    
    Returns:
        删除成功消息
    
    Raises:
        HTTPException: 如果角色不存在
    """
    result = db.execute(select(Role).where(Role.id == role_id))
    role = result.scalars().first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    db.delete(role)
    db.commit()
    
    return {"message": "Role deleted successfully"}
