from fastapi import FastAPI

from app.model.user import create_table as create_user_table, createUser
from app.model.status import create_table as create_status_table
from app.model.conversation import create_table as create_conversation_table

from app.router import router

app = FastAPI(title="mtaa")
app.include_router(router)

create_user_table()
create_status_table()
create_conversation_table()
# createUser(username="Patrik Fejda", email="patrikfejda@gmail.com")
