from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_properties():
    return {'message': 'Properties endpoint'}