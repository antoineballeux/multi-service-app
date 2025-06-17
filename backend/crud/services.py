# ─────────────────────────────────────────────
# 📂 crud/services.py — Service DB Operations
# ─────────────────────────────────────────────

from sqlmodel import Session, select
from models import Service
from logger import logger


def get_all_services(session: Session) -> list[Service]:
    """
    Retrieve all services from the database.

    Args:
        session (Session): Active database session.

    Returns:
        List[Service]: All available services.
    """
    logger.info("📥 Fetching all services")
    return session.exec(select(Service)).all()


def get_service_by_id(session: Session, service_id: int) -> Service | None:
    """
    Retrieve a service by its ID.

    Args:
        session (Session): Active database session.
        service_id (int): ID of the service to retrieve.

    Returns:
        Service | None: The found service or None if not found.
    """
    service = session.get(Service, service_id)
    if service:
        logger.info(f"📄 Service found (ID: {service_id})")
    else:
        logger.warning(f"⚠️ Service not found (ID: {service_id})")
    return service


def create_service(session: Session, service: Service) -> Service:
    """
    Add a new service to the database.

    Args:
        session (Session): Active database session.
        service (Service): The service object to insert.

    Returns:
        Service: The newly created and refreshed service object.
    """
    session.add(service)
    session.commit()
    session.refresh(service)
    logger.info(f"✅ Service created (ID: {service.id})")
    return service


def update_service(session: Session, db_service: Service, updated_data: Service) -> Service:
    """
    Update an existing service with new data.

    Args:
        session (Session): Active database session.
        db_service (Service): Existing service from the DB.
        updated_data (Service): New data to apply.

    Returns:
        Service: The updated and refreshed service object.
    """
    db_service.name = updated_data.name
    db_service.description = updated_data.description
    db_service.price = updated_data.price

    session.commit()
    session.refresh(db_service)
    logger.info(f"✏️ Service updated (ID: {db_service.id})")
    return db_service


def delete_service(session: Session, service: Service) -> None:
    """
    Permanently delete a service from the database.

    Args:
        session (Session): Active database session.
        service (Service): Service object to delete.

    Returns:
        None
    """
    session.delete(service)
    session.commit()
    logger.info(f"🗑️ Service deleted (ID: {service.id})")
