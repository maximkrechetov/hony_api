from fastapi import APIRouter

router = APIRouter()


@router.get('/health')
async def health_checker():
    return 'OK'


@router.get('/')
async def root():
    return 'Hello'
