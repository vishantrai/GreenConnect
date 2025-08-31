# this is for handling the post creation and post access 
from fastapi import APIRouter, status, Depends, HTTPException, Query
import schemas, models, oauth2
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional

router = APIRouter(
    prefix="/posts",
    tags = ["Posts"]
)

# route to create the post "SOMETHING NEW"
# basically we are creating the route for creating the post but here the problem is that we are taking input in two different tables so we have to create the route as the common details go to the common table and the other details go to the other table as per the post type 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), used_id: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict(exclude={"details"})) #here we are extracting the input details from the frontend and saving it to the post table we are excluding details as they are for other table 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    if post.post_type == "land_donor" and isinstance(post.details, schemas.LandDonor): #here we checking the post type and according to that we are sending the detail to that table, here the first case we are checking the post_type and the second thing which i am checking is the "isinstance()" it is a function which takes two values object and classname and then It checks if a given object is an instance (or subclass instance) of a particular class. here the post.details is the object for the landdonor class, isinstance will return true when the details will be instance of the class
        land_post = models.LandDonationPost(
            post_id = new_post.id, #here we are explicitly saving the post_id of the post in the landdonationpost table
            **post.details.dict()
        )
        db.add(land_post)
        db.commit()
        db.refresh(land_post)

    if post.post_type == "sapling_donor" and isinstance(post.details, schemas.SaplingDonor):
        sapling_post = models.SaplingDonor(
            post_id = new_post.id,
            **post.details.dict()
        )
        db.add(sapling_post)
        db.commit()
        db.refresh(sapling_post)

    if post.post_type == "equipment_donor" and isinstance(post.details, schemas.EquipmentDonor):
        equipment_post = models.EquipmentDonor(
            post_id = new_post.id,
            **post.details.dict()
        )
        db.add(equipment_post)
        db.commit()
        db.refresh(equipment_post)

    if post.post_type == "logistic_help" and isinstance(post.details, schemas.LogisticHelp):
        logistic_post = models.LogisticHelp(
            post_id = new_post.id,
            **post.details.dict()
        )
        db.add(logistic_post)
        db.commit()
        db.refresh(logistic_post)

    if post.post_type == "volunteers" and isinstance(post.details, schemas.Volunteers):
        volunteers_post = models.Volunteers(
            post_id = new_post.id,
            **post.details.dict()
        )
        db.add(volunteers_post)
        db.commit()
        db.refresh(volunteers_post)

    if post.post_type == "tree_care_request" and isinstance(post.details, schemas.TreeCareRequest):
        care_request_post = models.CareRequests(
            post_id = new_post.id,
            **post.details.dict()
        )
        db.add(care_request_post)
        db.commit()
        db.refresh(care_request_post)

    return new_post



# we want at the homepage we show all the post, if the user has enabled the location then based on the location if not then all the posts 
# we are creating the route for the getting the post, but there are multiple filters and we are implementing all at one route  *SOMETHING NEW*

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.PostOut])  #here the respone is in the form of list because their can be more than one post
def get_post( #here we are taking three optional values latitude, longitude, and filter and according to which we will show the posts
            lat: Optional[float] = Query(None, description="Latitude"), #here the description is used for the documentation 
            long: Optional[float] = Query(None, description="Longitude"), 
            filter: Optional[str] = Query(None, description="filter by type: land donor, sapling donor, volunteers, equipments, logistic, "), 
            db: Session = Depends(get_db)):
    #if we get a valid latitude and longitude then we will return the posts under the radius of 50 km
    if lat is not None and long is not None:
        radius_km = 50  # distance in kilometers

        # Haversine formula - isme jyada mind lgane ki jaroorat nhi hai ye jaisa hai waise hi chhor do
        posts = db.query(models.Post).filter( 
            func.acos(
                func.sin(func.radians(models.Post.latitude)) * func.sin(func.radians(lat)) +
                func.cos(func.radians(models.Post.latitude)) * func.cos(func.radians(lat)) *
                func.cos(func.radians(models.Post.longitude) - func.radians(long))
        ) * 6371 <= radius_km  # 6371 is Earth's radius in km
    )

    elif filter is not None:
        posts = db.query(models.Post).filter(models.Post.post_type == filter)
    else:
        posts = db.query(models.Post).all()

    if not posts:
        raise HTTPException(status_code=404, detail="No post found")

    return posts



#notes - ? ke baad likhe hue key-value pair ko query parameter bolte hain. Frontend (React, Angular, ya browser me user action) query params bhejta hai.
# Tum backend me bas ek "gate" khol rahe ho


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

