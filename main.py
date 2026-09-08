import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import Base, engine
from routes import analysis, wallets, reports

# Initialize SQL Database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FraudTrace API",
    description="Backend for Real-Time Identification of Fraud-Linked Cryptocurrency Wallets",
    version="2.0.0"
)

# CORS setup for web frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register modular routes
app.include_router(analysis.router)
app.include_router(wallets.router)
app.include_router(reports.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
