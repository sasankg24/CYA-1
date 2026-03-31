from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.dog import Dog
from app.schemas.dog import DogCreate, DogUpdate


def create_dog(db: Session, payload: DogCreate) -> Dog:
    dog = Dog(
        name=payload.name,
        age_years=payload.age_years,
        breed=payload.breed,
        color=payload.color,
    )
    db.add(dog)
    db.commit()
    db.refresh(dog)
    return dog


def list_dogs(db: Session, limit: int = 50, offset: int = 0) -> List[Dog]:
    return (
        db.query(Dog)
        .order_by(Dog.name.asc())
        .limit(limit)
        .offset(offset)
        .all()
    )


def get_dog(db: Session, dog_id: str) -> Optional[Dog]:
    # db.get works with PK; dog_id is a UUID string
    return db.get(Dog, dog_id)


def update_dog(db: Session, dog: Dog, patch: DogUpdate) -> Dog:
    patch_data = patch.model_dump(exclude_unset=True)

    for key, value in patch_data.items():
        setattr(dog, key, value)

    db.commit()
    db.refresh(dog)
    return dog


def delete_dog(db: Session, dog: Dog) -> None:
    db.delete(dog)
    db.commit()
