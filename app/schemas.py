from pydantic import BaseModel
from typing import Optional

# -------- Profile --------

class ProfileBase(BaseModel):
    first_name: Optional[str] = None
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    birth_date: Optional[str] = None
    phone_number: Optional[str] = None
    number_document: Optional[str] = None
    bank_account_number: Optional[str] = None
    interbank_account_number: Optional[str] = None

class ProfileUpdate(ProfileBase):
    pass  # mismo contenido, solo para semántica

class ProfileOut(ProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class BankAccountsOut(BaseModel):
    user_id: int
    bank_account_number: Optional[str]
    interbank_account_number: Optional[str]

# -------- Subscription status (respuesta compuesta) --------

class SubscriptionStatusOut(BaseModel):
    user_id: int
    has_subscription: bool
    status: Optional[str] = None
    plan_name: Optional[str] = None
    plan_price: Optional[float] = None
