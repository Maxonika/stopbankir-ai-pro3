# StopBankir AI PRO — Actions v2 — Render Deploy Ready

## Как деплоить на Render

### 1️⃣ Подготовь репозиторий

- Залей проект StopBankir AI PRO на GitHub (папка actions/ с main.py, swagger.yaml, .well-known/ai-plugin.json)

### 2️⃣ Создай Web Service на Render

- Render.com → New Web Service → Connect repo (stopbankir-ai-pro)
- Python 3.11 или новее
- Build Command → пусто
- Start Command:

```bash
uvicorn main:app --host=0.0.0.0 --port=10000
```

- Port → 10000
- Environment → Python

### 3️⃣ Проверка API

- Проверь что доступно:

```plaintext
https://ВАШ_RENDER_URL/.well-known/ai-plugin.json
https://ВАШ_RENDER_URL/swagger.yaml
```

### 4️⃣ Подключение в GPT Builder

- GPT Builder → Actions → Add Actions → Add Action via URL
- Вставляешь:

```plaintext
https://ВАШ_RENDER_URL/.well-known/ai-plugin.json
```

→ GPT подтягивает все Actions:

- /search_practice
- /calc_deadlines
- /check_case_status
- /check_counterparty
- /summarize_pdf
- /compare_positions
- /suggest_documents

### 5️⃣ Готово!