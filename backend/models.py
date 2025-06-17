from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone


# ─────────────────────────────────────────────
# 📦 Service model — defines one type of service the handyman offers
# ─────────────────────────────────────────────
class Service(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Auto-generated unique ID for the service"
    )
    name: str = Field(
        description="The display name of the service (e.g., 'TV Mounting')"
    )
    description: str = Field(
        description="Short explanation of what the service includes"
    )
    price: Optional[float] = Field(
        default=None,
        description="Optional price estimate for the service in dollars"
    )
    duration_min: Optional[int] = Field(
        default=None,
        description="Optional estimated time to complete the service, in minutes"
    )
    active: bool = Field(
        default=True,
        description="Indicates whether the service is available for booking"
    )

    # Back-reference to all bookings that reference this service
    bookings: List["Booking"] = Relationship(
        back_populates="service",
        sa_relationship_kwargs={"cascade": "delete"}  # optional for cleanup
    )


# ─────────────────────────────────────────────
# 📅 Booking model — represents a single booking request by a client
# ─────────────────────────────────────────────
class Booking(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Auto-generated unique ID for the booking"
    )
    name: str = Field(
        description="Client's full name"
    )
    email: str = Field(
        description="Client's email address"
    )
    phone: Optional[str] = Field(
        default=None,
        description="Optional client phone number for quick contact"
    )

    service_id: int = Field(
        foreign_key="service.id",
        description="ID of the selected service (foreign key to Service)"
    )
    service: Optional[Service] = Relationship(
        back_populates="bookings",
        sa_relationship_kwargs={"lazy": "selectin"}  # eager loading
    )

    message: Optional[str] = Field(
        default=None,
        description="Optional extra message from the client (e.g., notes or instructions)"
    )
    appointment_time: datetime = Field(
        description="The date and time the client wants to book the service"
    )
    status: str = Field(
        default="pending",
        description="Booking status: pending, confirmed, done, cancelled, etc."
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the booking was created (UTC)"
    )
