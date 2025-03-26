from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_chats():
    return {'message': 'Chat endpoint'}