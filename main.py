from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from database import engine,SessionLocal
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Home route
@app.get("/")
def home():
    return {"message": "BLOG API started"}

# Create Blog
@app.post("/create",response_model=schemas.BlogRespose)
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    new_blog=models.Blog(
        title=blog.title,
        content=blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blogs", response_model=list[schemas.BlogRespose])
def get_blogs(db:Session=Depends(get_db)):
    return db.query(models.Blog).all()
    
    
