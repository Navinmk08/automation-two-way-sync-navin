import logging
from fastapi import FastAPI

from sync_logic import run_sync

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/sync")
def trigger_sync():
    try:
        run_sync()
        return {"status": "synced"}
    except Exception as e:
        logger.exception("Sync failed")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    # run one sync pass
    run_sync()
