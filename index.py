from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json

app = FastAPI(title="StopBankir AI PRO Actions API v2")

# ВАЖНО: включаем CORS → GPT Builder теперь проверяет CORS на swagger.json
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

# Отдаём ai-plugin.json как JSON → НЕ FileResponse (иначе GPT Builder может ругаться)
@app.get("/.well-known/ai-plugin.json")
def get_ai_plugin():
    return JSONResponse({
        "schema_version": "v1",
        "name_for_human": "StopBankir AI Actions",
        "name_for_model": "stopbankir_actions",
        "description_for_model": "Actions for searching practice, checking deadlines, checking case status, counterparties, summarizing PDF, comparing positions and suggesting documents.",
        "api": {
            "type": "openapi",
            "url": "https://stopbankir-ai-pro3.onrender.com/swagger.json"
        },
        "auth": {
            "type": "none"
        },
        "logo_url": "https://your-site.com/logo.png",
        "contact_email": "your-email@example.com",
        "legal_info_url": "https://your-site.com/legal"
    })

# ОЧЕНЬ ВАЖНО → swagger.json отдаём как JSONResponse → иначе GPT Builder даст "Could not find valid URL in servers"
@app.get("/swagger.json")
def get_swagger_json():
    with open("swagger.json", "r", encoding="utf-8") as f:
        swagger = json.load(f)
    return JSONResponse(content=swagger)

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
            summary=f"Практика по '{req.query}', регион '{req.region}'"
        )
    ]
