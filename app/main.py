from fastapi import FastAPI
from .router import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     #all domains are allowed to talk to our API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(post.router)  # goes into the router folder to search and execute code
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")    #decorator using fastapi instance and http get method and root path(/) ->http://127.0.0.1:8000/
def root():
    return{"message": "WELCOME TO gujus-api!!!"}




    











