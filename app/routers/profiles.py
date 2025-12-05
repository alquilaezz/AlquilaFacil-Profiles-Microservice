from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db, get_current_user, CurrentUser
from ..clients.subscriptions_client import get_user_subscription_status_from_subscriptions

router = APIRouter(prefix="/api/v1/profiles", tags=["Profiles"])

# ----- Helpers -----

def _check_access(target_user_id: int, current_user: CurrentUser):
    if current_user.id != target_user_id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")

def _get_or_404_profile(user_id: int, db: Session) -> models.Profile:
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

# ----- Endpoints -----

@router.get("/user/{user_id}", response_model=schemas.ProfileOut)
def get_profile_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    _check_access(user_id, current_user)
    profile = _get_or_404_profile(user_id, db)
    return profile

@router.put("/{user_id}", response_model=schemas.ProfileOut)
def upsert_profile(
    user_id: int,
    payload: schemas.ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    _check_access(user_id, current_user)

    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    if not profile:
        profile = models.Profile(user_id=user_id)
        db.add(profile)
        db.flush()

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(profile, field, value)

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/bank-accounts/{user_id}", response_model=schemas.BankAccountsOut)
def get_bank_accounts(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    _check_access(user_id, current_user)
    profile = _get_or_404_profile(user_id, db)
    return schemas.BankAccountsOut(
        user_id=profile.user_id,
        bank_account_number=profile.bank_account_number,
        interbank_account_number=profile.interbank_account_number,
    )

@router.get("/subscription-status/{user_id}", response_model=schemas.SubscriptionStatusOut)
async def get_subscription_status(
    user_id: int,
    authorization: str = Header(...),
    current_user: CurrentUser = Depends(get_current_user),
):
    _check_access(user_id, current_user)

    sub = await get_user_subscription_status_from_subscriptions(
        user_id=user_id,
        authorization_header=authorization,
    )

    if not sub:
        return schemas.SubscriptionStatusOut(
            user_id=user_id,
            has_subscription=False,
        )

    return schemas.SubscriptionStatusOut(
        user_id=user_id,
        has_subscription=True,
        status=sub.get("subscription_status_id"),  # o mapea al nombre si lo cambias
        plan_name=str(sub.get("plan_id")),         # aquí podrías enriquecer llamando a /plan
        plan_price=None,
    )
