# this is for handling the post creation and post access 
from fastapi import APIRouter, status, Depends, HTTPException, Query
import schemas, models
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional

router = APIRouter(
    prefix="/posts",
    tags = ["Posts"]
)

# we want at the homepage we show all the post, if the user has enabled the location then based on the location if not then all the posts 
# we are creating the route for the getting the post, but there are multiple filters and we are implementing all at one route  *SOMETHING NEW*

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.PostOut])
def get_post(lat: Optional[float] = Query(None, description="Latitude"), #here the description is used for the documentation 
            long: Optional[float] = Query(None, description="Longitude"), 
            filter: Optional[str] = Query(None, description="filter by type: land donor, sapling donor, volunteers, equipments, logistic, "), 
            db: Session = Depends(get_db)):
    #if we get a valid latitude and longitude then we will return the posts under the radius of 50 km
    if lat is not None and long is not None:
        radius_km = 50  # distance in kilometers

        # Haversine formula
        data = db.query(models.Post).filter( 
            func.acos(
                func.sin(func.radians(models.Post.latitude)) * func.sin(func.radians(lat)) +
                func.cos(func.radians(models.Post.latitude)) * func.cos(func.radians(lat)) *
                func.cos(func.radians(models.Post.longitude) - func.radians(long))
        ) * 6371 <= radius_km  # 6371 is Earth's radius in km
    )

    elif filter is not None:
        data = db.query(models.Post).filter(models.Post.post_type == filter)

    posts = db.query(models.Post).all()

    if not posts:
        raise HTTPException(status_code=404, detail="No post found")

    return posts






# this below code was creating trouble in query and search so we have made single route for all posts

#land donors post route
# @router.post("/land_donor", status_code=status.HTTP_201_CREATED, response_model=schemas.LandDonorOut)
# def create_land_donor(post: schemas.LandDonor, db: Session = Depends (get_db)):
#     new_post = models.LandDonationPost(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return new_post

# #router which create the support donors
# @router.post("/supporter", status_code=status.HTTP_201_CREATED, response_model=schemas.SupportersOut)
# def create_supporters(post: schemas.CreatePost, db: Session = Depends(get_db)):
#     new_post = models.Supporters(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return new_post

# #now will be creating route for the different donor types each donor type can be accessed using the user_id
# @router.post("/supporter/{user_id}/sapling_donor", status_code=status.HTTP_201_CREATED, response_model=schemas.SupportersOut)
# def create_sapling_donation(user_id: int, post: schemas.SaplingDonor, db: Session = Depends(get_db)):
#     supporter = db.query(models.Supporters).filter(models.Supporters.id == user_id).first() #first()-Just give me the first matching result. Don’t flood me with a list
#     if not supporter:
#         raise HTTPException(status_code=404, detail="Supporter not found")
    
#     new_post = models.SaplingDonor(user_id = user_id,**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return new_post

