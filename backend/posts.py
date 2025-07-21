# this is for handling the post creation and post access 
from fastapi import APIRouter, status, Depends, HTTPException
import schemas, models
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(
    prefix="/posts",
    tags = ["Posts"]
)

Post = schemas.LandDonor

#land donors post route
@router.post("/land_donor", status_code=status.HTTP_201_CREATED, response_model=schemas.LandDonorOut)
def create_land_donor(post: schemas.LandDonor, db: Session = Depends (get_db)):
    new_post = models.LandDonationPost(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#router which create the support donors
@router.post("/supporter", status_code=status.HTTP_201_CREATED, response_model=schemas.SupportersOut)
def create_supporters(post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Supporters(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#now will be creating route for the different donor types each donor type can be accessed using the user_id
@router.post("/supporter/{user_id}/sapling_donor", status_code=status.HTTP_201_CREATED, response_model=schemas.SupportersOut)
def create_sapling_donation(user_id: int, post: schemas.SaplingDonor, db: Session = Depends(get_db)):
    supporter = db.query(models.Supporters).filter(models.Supporters.id == user_id).first() #first()-Just give me the first matching result. Don’t flood me with a list
    if not supporter:
        raise HTTPException(status_code=404, detail="Supporter not found")
    
    new_post = models.SaplingDonor(user_id = user_id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

