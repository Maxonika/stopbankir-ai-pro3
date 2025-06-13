from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="StopBankir AI PRO Actions API v2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return Response(content='{"status": "ok"}', media_type="application/json")

@app.get("/.well-known/ai-plugin.json")
def get_ai_plugin():
    return FileResponse(".well-known/ai-plugin.json", media_type="application/json")

@app.get("/swagger.json")
def get_swagger_json():
    return FileResponse("swagger.json", media_type="application/json")

# Action 1: Поиск судебной практики
class SearchRequest(BaseModel):
    query: str
    region: str

class CaseSummary(BaseModel):
    case_number: str
    court: str
    link: str
    summary: str

@app.post("/search_practice", response_model=List[CaseSummary])
def search_practice(req: SearchRequest):
    return [
        CaseSummary(
            case_number="А40-123456/2024",
            court="Арбитражный суд города Москвы",
            link="https://kad.arbitr.ru/Card/12345678",
            summary=f"Практика по '{req.query}', регион '{req.region}'."
        )
    ]