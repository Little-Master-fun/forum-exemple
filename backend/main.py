from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth_router, post_router, comment_router
from swagger_ui_bundle import swagger_ui_path  
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import applications

# 创建数据库表
Base.metadata.create_all(bind=engine)

def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui-bundle.min.js",
        swagger_css_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui.min.css")

applications.get_swagger_ui_html = swagger_monkey_patch



app = FastAPI(
    title="论坛 API",
    description="一个简单的论坛后端接口",
    version="1.0.0",
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
