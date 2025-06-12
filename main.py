from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta

app = FastAPI(title="StopBankir AI PRO Actions API v2")

@app.get("/.well-known/ai-plugin.json")
def get_ai_plugin():
    return FileResponse(".well-known/ai-plugin.json")

from fastapi.responses import Response

@app.get("/swagger.yaml", response_class=Response)
def get_swagger_yaml():
    with open("swagger.yaml", "r", encoding="utf-8") as f:
        content = f.read()
    return Response(content, media_type="application/yaml")

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
            summary="Иск об оспаривании сделки признан обоснованным."
        )
    ]

class DeadlineRequest(BaseModel):
    start_date: str
    days: int

class DeadlineResponse(BaseModel):
    end_date: str

@app.post("/calc_deadlines", response_model=DeadlineResponse)
def calc_deadlines(req: DeadlineRequest):
    start = datetime.strptime(req.start_date, "%Y-%m-%d")
    end = start + timedelta(days=req.days)
    return DeadlineResponse(end_date=end.strftime("%Y-%m-%d"))

class CaseStatusRequest(BaseModel):
    case_number: str

class CaseStatusResponse(BaseModel):
    status: str
    last_event: str

@app.post("/check_case_status", response_model=CaseStatusResponse)
def check_case_status(req: CaseStatusRequest):
    return CaseStatusResponse(
        status="В производстве",
        last_event="Апелляционная жалоба подана 05.06.2025"
    )

class CounterpartyRequest(BaseModel):
    inn: str

class CounterpartyResponse(BaseModel):
    bankruptcy_status: str
    fedresurs_publications: str
    court_cases_summary: str
    risk_assessment: str

@app.post("/check_counterparty", response_model=CounterpartyResponse)
def check_counterparty(req: CounterpartyRequest):
    return CounterpartyResponse(
        bankruptcy_status="Нет банкротства по данным на текущую дату.",
        fedresurs_publications="Публикации отсутствуют.",
        court_cases_summary="Есть 2 спора по договорам поставки.",
        risk_assessment="Умеренный риск."
    )

class PDFSummaryResponse(BaseModel):
    summary: str

@app.post("/summarize_pdf", response_model=PDFSummaryResponse)
async def summarize_pdf(file: UploadFile = File(...)):
    content = await file.read()
    return PDFSummaryResponse(summary="Резюме PDF: примерное содержание акта... (заглушка).")

class ComparePositionsRequest(BaseModel):
    text1: str
    text2: str

class ComparePositionsResponse(BaseModel):
    comparison_summary: str

@app.post("/compare_positions", response_model=ComparePositionsResponse)
def compare_positions(req: ComparePositionsRequest):
    return ComparePositionsResponse(
        comparison_summary="В первом тексте упор на доводы по ст. 61.2, во втором — акцент на отсутствие вины директора."
    )

class SuggestDocumentsRequest(BaseModel):
    user_role: str
    case_stage: str
    case_description: str

class SuggestDocumentsResponse(BaseModel):
    suggested_documents: List[str]

@app.post("/suggest_documents", response_model=SuggestDocumentsResponse)
def suggest_documents(req: SuggestDocumentsRequest):
    documents = [
        "Отзыв на заявление о субсидиарной ответственности",
        "Ходатайство об истребовании доказательств",
        "Ходатайство о снижении размера убытков",
        "Доказательства отсутствия контролирующего влияния"
    ]
    return SuggestDocumentsResponse(suggested_documents=documents)

from fastapi.responses import Response, FileResponse

# Корневой endpoint → чтобы HEAD / давал 200 OK
@app.get("/", response_class=Response)
def root():
    return Response(content='{"status": "ok"}', media_type="application/json")

# Сервис для .well-known/ai-plugin.json
@app.get("/.well-known/ai-plugin.json")
def get_ai_plugin():
    return FileResponse(".well-known/ai-plugin.json", media_type="application/json")

# Сервис для swagger.json
@app.get("/swagger.json")
def get_swagger_json():
    return FileResponse("swagger.json", media_type="application/json")

