from fastapi import FastAPI

from api.routers import user_routers, auth_routers, admin_routers

app = FastAPI()
app.include_router(admin_routers.router)
app.include_router(auth_routers.router)
app.include_router(user_routers.router)