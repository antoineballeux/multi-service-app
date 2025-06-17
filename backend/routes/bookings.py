# ─────────────────────────────────────────────
# 📂 routes/bookings.py — Booking Endpoints
# ─────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from models import Booking
from database import get_session
from auth import admin_required
from crud import bookings as crud_bookings
from logger import logger

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


# 📄 GET /bookings → List all bookings (admin only)
@router.get("/", response_model=List[Booking], dependencies=[Depends(admin_required)])
def list_bookings(session: Session = Depends(get_session)):
    """
    Retrieve a list of all bookings.

    Requires admin token.
    """
    try:
        logger.info("🔐 Admin requested full list of bookings.")
        return crud_bookings.get_all_bookings(session)
    except Exception as e:
        logger.error(f"❌ Failed to list bookings: {e}")
        raise HTTPException(status_code=500, detail="Could not retrieve bookings")


# 📄 GET /bookings/{id} → Get a booking by ID (admin only)
@router.get("/{id}", response_model=Booking, dependencies=[Depends(admin_required)])
def get_booking(id: int, session: Session = Depends(get_session)):
    """
    Retrieve a specific booking by ID.

    Requires admin token.
    """
    booking = crud_bookings.get_booking_by_id(session, id)
    if not booking:
        logger.warning(f"⚠️ Booking ID {id} not found.")
        raise HTTPException(status_code=404, detail="Booking not found")
    logger.info(f"📄 Booking ID {id} retrieved successfully.")
    return booking


# ➕ POST /bookings → Create a new booking (public)
@router.post("/", response_model=Booking, status_code=status.HTTP_201_CREATED)
def create_booking(booking: Booking, session: Session = Depends(get_session)):
    """
    Submit a new booking request.

    Public route. No authentication required.
    """
    try:
        new_booking = crud_bookings.create_booking(session, booking)
        logger.info(f"📬 New booking submitted (ID: {new_booking.id})")
        return new_booking
    except Exception as e:
        session.rollback()
        logger.error(f"❌ Failed to create booking: {e}")
        raise HTTPException(status_code=500, detail="Could not create booking")


# ✏️ PUT /bookings/{id} → Update a booking (admin only)
@router.put("/{id}", response_model=Booking, dependencies=[Depends(admin_required)])
def update_booking(id: int, updated_booking: Booking, session: Session = Depends(get_session)):
    """
    Update an existing booking.

    Requires admin token.
    """
    db_booking = crud_bookings.get_booking_by_id(session, id)
    if not db_booking:
        logger.warning(f"⚠️ Booking ID {id} not found for update.")
        raise HTTPException(status_code=404, detail="Booking not found")
    try:
        updated = crud_bookings.update_booking(session, db_booking, updated_booking)
        logger.info(f"✏️ Booking ID {id} updated.")
        return updated
    except Exception as e:
        session.rollback()
        logger.error(f"❌ Failed to update booking ID {id}: {e}")
        raise HTTPException(status_code=500, detail="Could not update booking")


# ❌ DELETE /bookings/{id} → Delete a booking (admin only)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(admin_required)])
def delete_booking(id: int, session: Session = Depends(get_session)):
    """
    Permanently delete a booking by ID.

    Requires admin token.
    """
    booking = crud_bookings.get_booking_by_id(session, id)
    if not booking:
        logger.warning(f"⚠️ Booking ID {id} not found for deletion.")
        raise HTTPException(status_code=404, detail="Booking not found")
    try:
        crud_bookings.delete_booking(session, booking)
        logger.info(f"🗑️ Booking ID {id} deleted.")
    except Exception as e:
        session.rollback()
        logger.error(f"❌ Failed to delete booking ID {id}: {e}")
        raise HTTPException(status_code=500, detail="Could not delete booking")
