from fastapi import APIRouter

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/pull-logs")
def pull_logs():
    return {
        "status": "scheduled",
        "note": "Placeholder: implement ISAPI/SDK pull here.",
    }
