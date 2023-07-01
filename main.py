from fastapi import FastAPI

# from app.some_service.controllers import router as some_service_router

app = FastAPI()

# app.include_router(some_service_router)


@app.get("/", tags=["health"], operation_id="check", response_model=str)
def index() -> str:
    return "ok"
