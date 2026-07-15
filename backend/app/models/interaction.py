from sqlalchemy import Column, Integer, String, Date, Time

from app.database.database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)

    doctor_name = Column(String, nullable=False)

    hospital = Column(String)

    interaction_type = Column(String)

    interaction_date = Column(Date)

    interaction_time = Column(Time)

    discussion = Column(String)

    follow_up = Column(String)
    