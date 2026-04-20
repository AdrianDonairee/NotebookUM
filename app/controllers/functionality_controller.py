from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.models.functionality_model import FunctionalityCreate, FunctionalityUpdate
from app.services.functionality_service import FunctionalityService


router = APIRouter(prefix="/api/v1/funcionalidades", tags=["funcionalidades"])
functionality_service = FunctionalityService()


@router.get("/")
def get_all_functionalities():
    data = functionality_service.get_all()
    return {"success": True, "data": data}


@router.get("/{functionality_id}")
def get_functionality(functionality_id: int):
    data = functionality_service.get_by_id(functionality_id)
    if data is None:
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": "Not found"},
        )

    return {"success": True, "data": data}


@router.post("/", status_code=201)
def create_functionality(payload: FunctionalityCreate):
    data = functionality_service.create(payload)
    return {"success": True, "data": data}


@router.put("/{functionality_id}")
def update_functionality(functionality_id: int, payload: FunctionalityUpdate):
    data = functionality_service.update(functionality_id, payload)
    if data is None:
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": "Not found"},
        )

    return {"success": True, "data": data}


@router.delete("/{functionality_id}")
def delete_functionality(functionality_id: int):
    deleted = functionality_service.delete(functionality_id)
    if not deleted:
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": "Not found"},
        )

    return {"success": True, "message": "Deleted successfully"}
