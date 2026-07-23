"""
用户相关路由 —— 全部以 /users 开头
"""
from fastapi import APIRouter  # ← 跟 FastAPI 用法一样，但不是 app = FastAPI()

# =====================================================================
# 创建路由器实例
# =====================================================================
# prefix="/users"    → 此文件所有路由自动加 /users 前缀
# tags=["用户管理"]   → 在 /docs 文档里分组显示
router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("/")
async def list_users():
    """实际访问路径：/users/"""
    return {"msg": "用户列表"}


@router.get("/{user_id}")
async def get_user(user_id: int):
    """实际访问路径：/users/123"""
    return {"msg": f"用户详情", "user_id": user_id}


@router.post("/")
async def create_user(name: str, email: str):
    """实际访问路径：/users/"""
    return {"msg": "创建用户成功", "name": name, "email": email}
