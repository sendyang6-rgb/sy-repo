from fastapi import FastAPI, Path, Query, Depends, Header
from typing import Annotated  # 注解
from pydantic import BaseModel, Field

# =====================================================================
# 🔶 导入子路由器
# =====================================================================
from routers.users import router as user_router        # 用户模块
from routers.articles import router as article_router   # 文章模块

app = FastAPI()


# =====================================================================
# 🔶 挂载子路由器 —— 核心就是 app.include_router()
# =====================================================================
# 子路由器里已经定义了 prefix="/users"，这里的路由直接继承那个前缀
app.include_router(user_router)
app.include_router(article_router)
# 也可以在这里覆盖或追加 prefix：
# app.include_router(user_router, prefix="/api/v1")   → /api/v1/users/


# =====================================================================
# 🔶 APIRouter 对比：app.xxx vs router.xxx
# =====================================================================
#            main.py                     routers/users.py
#       ┌─────────────────┐         ┌─────────────────────┐
#       │ app = FastAPI() │         │ router = APIRouter( │
#       │ app.get(...)    │         │   prefix="/users")  │
#       │ app.post(...)   │         │ router.get(...)     │
#       │                 │         │ router.post(...)    │
#       │ app.include_    │ ◄────── │                     │
#       │   router(user)  │  挂载    └─────────────────────┘
#       └─────────────────┘
#
# 用法一模一样，只是把 app 换成 router，最后用 include_router 挂到主 app 上


# =====================================================================
# 🔶 依赖注入相关（之前学的，保留完整）
# =====================================================================
# 路由函数需要某些"前置工作"才能运行，比如：
#   - 校验参数
#   - 检查权限
#   - 连接数据库
#   - 获取当前用户
#
# 传统写法：每个路由里都重复写一遍这些代码
# 依赖注入：把这些"前置工作"抽成一个函数，通过 Depends() 注入到路由里
# FastAPI 会在你的路由执行前自动运行它们


async def common_parameters(
    page: int = 1,
    size: int = 10
):
    """
    通用的分页参数
    多个路由都用分页时，不用每个路由都写一遍 page 和 size
    """
    return {"page": page, "size": size}


@app.get("/items/")
async def list_items(
    params: Annotated[dict, Depends(common_parameters)]  # ← 注入依赖
):
    return {"msg": "物品列表", **params}


class PaginationParams:
    """把分页参数封装成类"""
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="页码"),
        size: int = Query(default=10, ge=1, le=100, description="每页条数")
    ):
        self.page = page
        self.size = size


@app.get("/books/")
async def list_books(pagination: Annotated[PaginationParams, Depends(PaginationParams)]):
    return {"msg": "书籍列表", "page": pagination.page, "size": pagination.size}


async def get_current_user(
    x_token: Annotated[str | None, Header()] = None  # ← 可选 header，默认 None
):
    """模拟认证：检查请求头里的 x-token"""
    if x_token is None:
        return {"user_id": 0, "username": "匿名用户"}
    if x_token == "secret-token":
        return {"user_id": 1, "username": "SY"}
    return {"user_id": 0, "username": "无效token"}


@app.get("/me")
async def read_current_user(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    return {"msg": "当前登录用户", "user": current_user}


async def get_db_connection():
    """模拟数据库连接"""
    return {"connected": True, "db_name": "test_db"}


async def get_user_repo(
    db: Annotated[dict, Depends(get_db_connection)]  # 子依赖
):
    """模拟用户仓库"""
    return {"db": db, "table": "users"}


@app.get("/repo-test")
async def test_repo(
    repo: Annotated[dict, Depends(get_user_repo)]
):
    return {"msg": "依赖链测试", "repo": repo}


# =====================================================================
# 🔶 根路由 & 基础路由
# =====================================================================
@app.get("/")
async def hello():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def hello_name(name: str):
    return {"message": f"Hello {name}"}


@app.get("/p/{article_id}")
async def article_detail(article_id: Annotated[int, Path(ge=2)]):
    return {"article_id": article_id}


# ==================== 查询传参（Query Parameters）====================
@app.get("/article/list")
async def article_list(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=10)] = 10
):
    return {"page": page, "size": size}


# ==================== POST：请求体（Request Body）====================
class LoginIn(BaseModel):
    email: Annotated[str, Field(..., description="邮箱")]
    password: Annotated[str, Field(..., min_length=5, max_length=12, description="密码")]


@app.post("/login")
async def Login(data: LoginIn):
    email = data.email
    password = data.password
    return {"email": email, "password": password}


async def page_common(page: int = 0, size: int = 10):
    return {"page": page, "size": size}


@app.get("/user/list")
async def get_user_list(
    page_params: Annotated[dict, Depends(page_common)]
):
    return {"msg": "信息", **page_params}


