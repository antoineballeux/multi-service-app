# ─────────────────────────────────────────────
# 📂 routes/services.py — Service Endpoints
# ─────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from models import Service
from database import get_session
from auth import admin_required
from crud import services as crud_services
from logger import logger

router = APIRouter(
    prefix="/services",
    tags=["Services"]
)


# 📄 GET /services → List all available services (public)
@router.get("/", response_model=List[Service])
def list_services(session: Session = Depends(get_session)):
    """
    Retrieve a list of all available services.

    Public route. No authentication required.
    """
    try:
        logger.info("📦 Public request to list all services")
        return crud_services.get_all_services(session)
    except Exception as e:
        logger.error(f"❌ Failed to list services: {e}")
        raise HTTPException(status_code=500, detail="Could not retrieve services")


# 📄 GET /services/{id} → Get a specific service by ID (admin only)
@router.get("/{id}", response_model=Service, dependencies=[Depends(admin_required)])
def get_service(id: int, session: Session = Depends(get_session)):
    """
    Retrieve a single service by its ID.

    Requires admin token.
    """
    service = crud_services.get_service_by_id(session, id)
    if not service:
        logger.warning(f"⚠️ Service ID {id} not found")
        raise HTTPException(status_code=404, detail="Service not found")
    logger.info(f"🔍 Retrieved service ID {id}")
    return service


# ➕ POST /services → Create a new service (admin only)
@router.post("/", response_model=Service, status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_required)])
def create_service(service: Service, session: Session = Depends(get_session)):
    """
    Create and store a new service.

    Requires admin token.
    """
    try:
        new_service = crud_services.create_service(session, service)
        logger.info(f"✅ Created new service with ID {new_service.id}")
        return new_service
    except Exception as e:
        session.rollback()
        logger.error(f"❌ Failed to create service: {e}")
        raise HTTPException(status_code=500, detail="Could not create service")


# ✏️ PUT /services/{id} → Update a service (admin only)
@router.put("/{id}", response_model=Service, dependencies=[Depends(admin_required)])
def update_service(id: int, updated_service: Service, session: Session = Depends(get_session)):
    """
    Update an existing service.

    Requires admin token.
    """
    db_service = crud_services.get_service_by_id(session, id)
    if not db_service:
        logger.warning(f"⚠️ Service ID {id} not found for update")
        raise HTTPException(status_code=404, detail="Service not found")
    try:
        updated = crud_services.update_service(session, db_service, updated_service)
        logger.info(f"✏️ Updated service ID {id}")
        return updated
    except Exception as e:
        session.rollback()
        logger.error(f"❌ Failed to update service ID {id}: {e}")
        raise HTTPException(status_code=500, detail="Could not update service")


# ❌ DELETE /services/{id} → Delete a service (admin only)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(admin_required)])
def delete_service(id: int, session: Session = Depends(get_session)):
    """
    Permanently delete a service by ID.

    Requires admin token.
    """
    service = crud_services.get_service_by_id(session, id)
    if not service:
        logger.warning(f"⚠️ Service ID {id} not found for deletion")
        raise HTTPException(status_code=404, detail="Service not found")
    try:
        crud_services.delete_service(session, service)
        logger.info(f"🗑️ Deleted service ID {id}")
    except Exception as e:
        session.rollback()
        logger.error(f"❌ Failed to delete service ID {id}: {e}")
        raise HTTPException(status_code=500, detail="Could not delete service")
