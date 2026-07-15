from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.interaction import Interaction
from app.schemas.interaction import InteractionCreate, InteractionResponse

router = APIRouter(tags=["Interactions"])


# Create Interaction
@router.post("/interactions")
def create_interaction(
    interaction: InteractionCreate,
    db: Session = Depends(get_db)
):
    new_interaction = Interaction(
        doctor_name=interaction.doctor_name,
        hospital=interaction.hospital,
        interaction_type=interaction.interaction_type,
        interaction_date=interaction.interaction_date,
        interaction_time=interaction.interaction_time,
        discussion=interaction.discussion,
        follow_up=interaction.follow_up
    )

    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)

    return {
        "message": "Interaction saved successfully",
        "id": new_interaction.id
    }


# Get All Interactions
@router.get("/interactions", response_model=list[InteractionResponse])
def get_interactions(db: Session = Depends(get_db)):
    return db.query(Interaction).all()


# Update Interaction
@router.put("/interactions/{interaction_id}")
def update_interaction(
    interaction_id: int,
    updated_data: InteractionCreate,
    db: Session = Depends(get_db)
):
    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id
    ).first()

    if interaction is None:
        raise HTTPException(status_code=404, detail="Interaction not found")

    interaction.doctor_name = updated_data.doctor_name
    interaction.hospital = updated_data.hospital
    interaction.interaction_type = updated_data.interaction_type
    interaction.interaction_date = updated_data.interaction_date
    interaction.interaction_time = updated_data.interaction_time
    interaction.discussion = updated_data.discussion
    interaction.follow_up = updated_data.follow_up

    db.commit()
    db.refresh(interaction)

    return {
        "message": "Interaction updated successfully",
        "interaction": interaction
    }


# Delete Interaction
@router.delete("/interactions/{interaction_id}")
def delete_interaction(
    interaction_id: int,
    db: Session = Depends(get_db)
):
    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id
    ).first()

    if interaction is None:
        raise HTTPException(status_code=404, detail="Interaction not found")

    db.delete(interaction)
    db.commit()

    return {
        "message": "Interaction deleted successfully"
    }