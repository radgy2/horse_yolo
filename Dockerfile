FROM python:3.10-slim

WORKDIR /app

# opencv용 (PIL은 필요없지만 ultralytics/opencv 때문에)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# src만 복사 (모델(best.pt)도 src 안에 있으니 같이 들어감)
COPY src ./src

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# 30초마다, 5초 안에, /health를 호출해서 3번 연속 실패하면 “이 컨테이너 문제 있음”이라고 표시
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1
