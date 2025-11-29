from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth_router, post_router, comment_router

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="论坛 API",
    description="一个简单的论坛后端接口",
    version="1.0.0",
    swagger_ui_parameters={
        "url": "/openapi.json",
    },
    # 使用国内 CDN
    swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.9.0/swagger-ui-bundle.js",
    swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.9.0/swagger-ui.css",
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
