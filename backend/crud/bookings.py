# ─────────────────────────────────────────────
# 📂 crud/bookings.py — Booking DB Operations
# ─────────────────────────────────────────────

from sqlmodel import Session, select
from models import Booking
from logger import logger


def get_all_bookings(session: Session) -> list[Booking]:
    """
    Retrieve all bookings from the database.

    Args:
        session (Session): Active database session.

    Returns:
        List[Booking]: All booking entries.
    """
    logger.info("📥 Fetching all bookings")
    return session.exec(select(Booking)).all()


def get_booking_by_id(session: Session, booking_id: int) -> Booking | None:
    """
    Retrieve a single booking by its ID.

    Args:
        session (Session): Active database session.
        booking_id (int): ID of the booking to retrieve.

    Returns:
        Booking | None: The found booking or None if not found.
    """
    booking = session.get(Booking, booking_id)
    if booking:
        logger.info(f"📄 Booking found (ID: {booking_id})")
    else:
        logger.warning(f"⚠️ Booking not found (ID: {booking_id})")
    return booking


def create_booking(session: Session, booking: Booking) -> Booking:
    """
    Add a new booking to the database.

    Args:
        session (Session): Active database session.
        booking (Booking): The booking object to insert.

    Returns:
        Booking: The newly created and refreshed booking object.
    """
    session.add(booking)
    session.commit()
    session.refresh(booking)
    logger.info(f"✅ Booking created (ID: {booking.id})")
    return booking


def update_booking(session: Session, db_booking: Booking, updated_data: Booking) -> Booking:
    """
    Update an existing booking with new data.

    Args:
        session (Session): Active database session.
        db_booking (Booking): Existing booking from the DB.
        updated_data (Booking): New data to apply.

    Returns:
        Booking: The updated and refreshed booking object.
    """
    db_booking.name = updated_data.name
    db_booking.email = updated_data.email
    db_booking.phone = updated_data.phone
    db_booking.service_id = updated_data.service_id
    db_booking.message = updated_data.message
    db_booking.appointment_time = updated_data.appointment_time

    session.commit()
    session.refresh(db_booking)
    logger.info(f"✏️ Booking updated (ID: {db_booking.id})")
    return db_booking


def delete_booking(session: Session, booking: Booking) -> None:
    """
    Permanently delete a booking from the database.

    Args:
        session (Session): Active database session.
        booking (Booking): Booking object to delete.

    Returns:
        None
    """
    session.delete(booking)
    session.commit()
    logger.info(f"🗑️ Booking deleted (ID: {booking.id})")
