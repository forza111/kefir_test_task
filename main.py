from fastapi import FastAPI

from routers import admin_routers,auth_routers,user_routers


app = FastAPI()
app.include_router(admin_routers.router)
app.include_router(auth_routers.router)
app.include_router(user_routers.router)