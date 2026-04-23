from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.gambler_service import GamblerService

app = FastAPI()
gambler_service = GamblerService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later you can restrict to http://localhost:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GamblerCreateRequest(BaseModel):
    gambler_id: int
    username: str
    full_name: str
    email: str
    initial_stake: float
    win_threshold: float
    loss_threshold: float
    min_required_stake: float


@app.get("/")
def home():
    return {"message": "Backend running successfully"}


@app.get("/gamblers")
def get_all_gamblers():
    gamblers = gambler_service.get_all_gamblers()
    return gamblers


@app.get("/gamblers/{gambler_id}")
def get_gambler(gambler_id: int):
    gambler = gambler_service.get_gambler(gambler_id)

    if not gambler:
        raise HTTPException(status_code=404, detail="Gambler not found")

    return gambler


@app.post("/gamblers")
def create_gambler(data: GamblerCreateRequest):
    existing = gambler_service.get_gambler(data.gambler_id)
    if existing:
        raise HTTPException(status_code=400, detail="Gambler ID already exists")

    gambler_service.create_gambler(
        data.gambler_id,
        data.username,
        data.full_name,
        data.email,
        data.initial_stake,
        data.win_threshold,
        data.loss_threshold,
        data.min_required_stake,
    )

    return {"message": "Gambler created successfully"}