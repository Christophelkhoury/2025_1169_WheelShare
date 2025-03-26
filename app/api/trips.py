from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_trips():
    return {'message': 'Trips endpoint'}