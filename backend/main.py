from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth_router, post_router, comment_router
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from swagger_ui_bundle import swagger_ui_path  

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="论坛 API",
    description="一个简单的论坛后端接口",
    version="1.0.0",
    docs_url=None,     # 一定要是 None
    redoc_url=None,
)

# 挂载 Swagger UI 的静态文件到 /swagger-static
app.mount("/swagger-static", StaticFiles(directory=swagger_ui_path), name="swagger-static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="论坛 API 文档",
        swagger_js_url="/swagger-static/swagger-ui-bundle.js",
        swagger_css_url="/swagger-static/swagger-ui.css",
        swagger_favicon_url="/swagger-static/favicon-32x32.png",
    )

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)


@app.get("/")
def root():
    return {"message": "欢迎使用论坛 API", "docs": "/docs"}
