from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from auth import create_token, verify_credentials, verify_token
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm
import schemas
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "BLOG API started"}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not verify_credentials(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return {
        "access_token": create_token({"sub": form_data.username}),
        "token_type": "bearer",
    }


@app.post("/create", response_model=schemas.BlogRespose)
def create_blog(
    blog: schemas.BlogCreate,
    db: Session = Depends(get_db),
    _user=Depends(verify_token),
):
    new_blog = models.Blog(
        title=blog.title,
        content=blog.content,
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blogs", response_model=list[schemas.BlogRespose])
def get_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


@app.get("/blogs/{blog_id}", response_model=schemas.BlogRespose)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="blog not found")
    return blog


@app.put("/edit/{id}", response_model=schemas.BlogRespose)
def edit_blog(
    id: int,
    blog: schemas.BlogCreate,
    db: Session = Depends(get_db),
    _user=Depends(verify_token),
):
    existing_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not existing_blog:
        raise HTTPException(status_code=404, detail="invalid id number")
    existing_blog.content = blog.content
    existing_blog.title = blog.title

    db.commit()
    db.refresh(existing_blog)
    return existing_blog


@app.delete("/delete/{id}")
def delete_blog(
    id: int,
    db: Session = Depends(get_db),
    _user=Depends(verify_token),
):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="invalid id")
    db.delete(blog)
    db.commit()
    return {"message": "BLOG deleted successfully"}