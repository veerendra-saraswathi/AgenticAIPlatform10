from fastapi import FastAPI

from api.fraud_api import router as fraud_router

app = FastAPI(
    title="AgenticAIPlatform10",
    description="Enterprise Agentic AI Platform",
    version="1.0.0",
)

# Register routers
app.include_router(fraud_router)


@app.get("/health")
def health():
    return {"status": "ok"}
