FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run Playwright install if browser MCP is needed in docker
# RUN playwright install --with-deps

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
