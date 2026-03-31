from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.dog import DogCreate, DogUpdate, DogOut
from app import crud

router = APIRouter(prefix="/dogs", tags=["dogs"])


def to_out(dog) -> DogOut:
    return DogOut(
        id=str(dog.id),
        name=dog.name,
        age_years=dog.age_years,
        breed=dog.breed,
        color=dog.color,
    )


@router.post("", response_model=DogOut, status_code=status.HTTP_201_CREATED)
def create_dog(payload: DogCreate, db: Session = Depends(get_db)) -> DogOut:
    dog = crud.dog.create_dog(db, payload)
    return to_out(dog)


@router.get("", response_model=List[DogOut])
def list_dogs(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
) -> List[DogOut]:
    dogs = crud.dog.list_dogs(db, limit=limit, offset=offset)
    return [to_out(d) for d in dogs]


@router.get("/{dog_id}", response_model=DogOut)
def get_dog(dog_id: str, db: Session = Depends(get_db)) -> DogOut:
    dog = crud.dog.get_dog(db, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    return to_out(dog)


@router.patch("/{dog_id}", response_model=DogOut)
def update_dog(dog_id: str, patch: DogUpdate, db: Session = Depends(get_db)) -> DogOut:
    dog = crud.dog.get_dog(db, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")

    updated = crud.dog.update_dog(db, dog, patch)
    return to_out(updated)


@router.delete("/{dog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dog(dog_id: str, db: Session = Depends(get_db)) -> None:
    dog = crud.dog.get_dog(db, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")

    crud.dog.delete_dog(db, dog)
    return
