# 汇总的路由注册route_register.py
from fastapi import APIRouter

from . import auth, users, archive, knowledge

router = APIRouter()

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(archive.router)
router.include_router(knowledge.router)


def register_routes(app):
    app.include_router(router)

