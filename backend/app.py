from fastapi import FastAPI
import uvicorn
from routers.report_router import router as report_router
def main():
    app = FastAPI()
    app.include_router(report_router)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )

if __name__ == "__main__":
    main()