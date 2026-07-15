from datetime import date, time
from typing import Optional

from langchain_core.tools import tool
from sqlalchemy.orm import Session

from app.models.interaction import Interaction


def make_tools(db: Session):
    """Build the CRM tool set bound to a single request-scoped db session."""

    @tool
    def log_interaction(
        doctor_name: str,
        hospital: str,
        interaction_type: str,
        interaction_date: str,
        interaction_time: str,
        discussion: str,
        follow_up: str = "",
    ) -> str:
        """Log a new doctor interaction in the CRM."""
        interaction = Interaction(
            doctor_name=doctor_name,
            hospital=hospital,
            interaction_type=interaction_type,
            interaction_date=date.fromisoformat(interaction_date),
            interaction_time=time.fromisoformat(interaction_time),
            discussion=discussion,
            follow_up=follow_up,
        )
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
        return f"Logged interaction #{interaction.id} with Dr. {doctor_name}."

    @tool
    def search_interactions(doctor_name: str) -> str:
        """Search past interactions by doctor name."""
        results = (
            db.query(Interaction)
            .filter(Interaction.doctor_name.ilike(f"%{doctor_name}%"))
            .all()
        )
        if not results:
            return f"No interactions found for {doctor_name}."
        return "\n".join(
            f"#{r.id} | {r.doctor_name} @ {r.hospital} on {r.interaction_date}: {r.discussion}"
            for r in results
        )

    @tool
    def generate_summary() -> str:
        """Summarize all logged interactions."""
        interactions = db.query(Interaction).all()
        if not interactions:
            return "No interactions found."
        return "\n\n".join(
            f"Doctor: {i.doctor_name}\nHospital: {i.hospital}\nDiscussion: {i.discussion}"
            for i in interactions
        )

    @tool
    def edit_interaction(
        interaction_id: int,
        new_discussion: Optional[str] = None,
        new_follow_up: Optional[str] = None,
    ) -> str:
        """Edit an existing interaction's discussion or follow-up note by its ID."""
        interaction = (
            db.query(Interaction).filter(Interaction.id == interaction_id).first()
        )
        if not interaction:
            return f"Interaction #{interaction_id} not found."

        # Use "is not None" (not truthiness) so callers can intentionally
        # clear a field by passing an empty string.
        if new_discussion is not None:
            interaction.discussion = new_discussion
        if new_follow_up is not None:
            interaction.follow_up = new_follow_up

        db.commit()
        db.refresh(interaction)
        return f"Interaction #{interaction_id} has been successfully updated."

    @tool
    def delete_interaction(interaction_id: int) -> str:
        """Delete an interaction from the CRM by its ID."""
        interaction = (
            db.query(Interaction).filter(Interaction.id == interaction_id).first()
        )
        if not interaction:
            return f"Interaction #{interaction_id} not found."

        db.delete(interaction)
        db.commit()
        return f"Interaction #{interaction_id} has been deleted."

    return [
        log_interaction,
        search_interactions,
        generate_summary,
        edit_interaction,
        delete_interaction,
    ]
