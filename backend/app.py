from fastapi import FastAPI
from routers.report_router import router as report_router
def main():
    app = FastAPI()
    app.include_router(report_router)

if __name__ == "__main__":
    main()