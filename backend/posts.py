# this is for handling the post creation and post access 
from fastapi import APIRouter, status, Depends
import schemas, models
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(
    prefix="/posts",
    tags = ["Posts"]
)

Post = schemas.LandDonor

@router.post("/land_donor", status_code=status.HTTP_201_CREATED, response_model=schemas.LandDonorOut)
def create_land_donor(post: schemas.LandDonor, db: Session = Depends (get_db)):
    new_post = models.LandDonationPost(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post