import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, database, utils
from routers import tasks, users 

# Database tables banana
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="TaskFlow Pro",
    description="A High-Performance Task Management API with JWT Security & Server-Side Pagination.",
    version="1.5.0",
    contact={
        "name": "Sarthak Tiwari",
        "email": "your-email@example.com",
    }
)

# Ek hi baar CORS settings kaafi hain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers include karna
app.include_router(tasks.router)
app.include_router(users.router)

@app.get("/")
def home():
    return {"message": "Sarthak bhai, Backend ekdum mast chal raha hai!"}

@app.post("/login", tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not user or not utils.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Galat Email ya Password")
    
    token = utils.create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)