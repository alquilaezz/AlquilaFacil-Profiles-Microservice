from sqlalchemy import Column, Integer, Text
from .database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(Text, nullable=True)
    father_name = Column(Text, nullable=True)
    mother_name = Column(Text, nullable=True)
    birth_date = Column(Text, nullable=True)  # podrías cambiarlo a DateTime si quieres
    phone_number = Column(Text, nullable=True)
    number_document = Column(Text, nullable=True)
    bank_account_number = Column(Text, nullable=True)
    interbank_account_number = Column(Text, nullable=True)
    user_id = Column(Integer, nullable=False, index=True, unique=True)
