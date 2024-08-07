from fastapi import FastAPI

from server.database import Base, engine
from server.modules.user.routes import router as user_router
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, SecurityScheme as SecuritySchemeModel
from fastapi.openapi.models import OAuthFlowPassword as OAuthFlowPasswordModel
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi

app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(user_router)


@app.get('/')
def homepage():
    return {"Message": "Welcome to our app"}
