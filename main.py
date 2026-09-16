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

@app.get("/blogs/{blog_id}",response_model=schemas.BlogRespose)
def get_blog(blog_id:int,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if not blog:
        raise HTTPException(status_code=404,detail="blog not found")
    return blog

@app.put("/edit/{id}",response_model=schemas.BlogRespose)
def edit_blog(id:int,blog:schemas.BlogCreate,db:Session=Depends(get_db)):
    existing_blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not existing_blog:
        raise HTTPException(status_code=404,detail="invalid id number")
    existing_blog.content=blog.content
    existing_blog.title=blog.title
    
    db.commit()
    db.refresh(existing_blog)
    return existing_blog
@app.delete("/delete/{id}")
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=404,detail="invalid id")
    db.delete(blog)
    db.commit()
    return {"message":"BLOG deleted successfully"}