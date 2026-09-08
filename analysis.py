from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from schemas.wallet import WalletAnalysisResponse
from services.blockchain import fetch_live_transactions
from services.risk_engine import evaluate_risk

router = APIRouter(prefix="/api/v1", tags=["Analysis"])

@router.get("/analyze", response_model=WalletAnalysisResponse)
async def analyze_wallet(
    address: str = Query(..., description="Target Ethereum wallet address"),
    blockchain: str = Query("Ethereum", description="Selected blockchain network"),
    db: Session = Depends(get_db)
):
    if not address.startswith("0x") or len(address) != 42:
        raise HTTPException(status_code=400, detail="Invalid Ethereum wallet address format.")

    raw_transactions = fetch_live_transactions(address)
    metrics = evaluate_risk(address, raw_transactions, db)

    return WalletAnalysisResponse(
        wallet_address=address,
        blockchain=blockchain,
        risk_score=metrics["score"],
        risk_status=metrics["status"],
        suspicious_transactions_count=metrics["suspicious_count"],
        fraud_indicators=metrics["indicators"],
        connected_wallets=metrics["connected_wallets"],
        transactions=metrics["parsed_txs"]
    )
