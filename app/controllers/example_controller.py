from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from ..services.example_service import ExampleService

router = APIRouter(prefix='/api/example', tags=['example'])
example_service = ExampleService()


@router.get('/')
def get_all():
    data = example_service.get_all()
    return {'success': True, 'data': data}


@router.get('/{id}')
def get_one(id):
    data = example_service.get_by_id(id)
    if data:
        return {'success': True, 'data': data}
    return JSONResponse(status_code=404, content={'success': False, 'message': 'Not found'})


@router.post('/', status_code=201)
def create(data: dict = Body(default_factory=dict)):
    result = example_service.create(data)
    return {'success': True, 'data': result}


@router.put('/{id}')
def update(id, data: dict = Body(default_factory=dict)):
    result = example_service.update(id, data)
    if result:
        return {'success': True, 'data': result}
    return JSONResponse(status_code=404, content={'success': False, 'message': 'Not found'})


@router.delete('/{id}')
def delete(id):
    result = example_service.delete(id)
    if result:
        return {'success': True, 'message': 'Deleted successfully'}
    return JSONResponse(status_code=404, content={'success': False, 'message': 'Not found'})