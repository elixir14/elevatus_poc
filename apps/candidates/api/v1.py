from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_candidates():
    return "candidates app created!"
