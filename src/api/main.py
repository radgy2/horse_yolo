import io
import os
import time
import logging
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image, ImageDraw
from ultralytics import YOLO
app = FastAPI(max_request_size=10 * 1024 * 1024)  # 10MB 넘는 요청 → 자동으로 차단 (대용량 이미지 차단)

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parents[1]  # project-root (src의 상위)
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))  # 앞으로 HTML 템플릿 파일은 모두 이 폴더 안에서 찾겟다는 의미

LOG_DIR = PROJECT_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("horse-api")

model = None  # 🔥 여기서만 선언


@app.on_event("startup")
# 모델 로드, FastAPI 서버가 켜질 때 딱 한 번 실행
def startup_event():
    global model

    model_path = PROJECT_DIR / "src/model/saved/best.pt"
    logger.info(f"SERVER_START | loading_model={model_path}")

    if not model_path.exists():
        logger.error("MODEL_LOAD_FAIL | model file not found")
        raise RuntimeError("Model file not found")

    model = YOLO(str(model_path))
    logger.info("MODEL_LOADED | status=SUCCESS")


@app.get("/health")
# /health 엔드포인트 (운영용)
def health():
    return {
        "status": "ok",  # 서버 살아있나?
        "model_loaded": model is not None  # 모델 정상 로드됐나?
    }


@app.get("/", response_class=HTMLResponse)
# / 엔드포인트 (웹 화면)
async def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})  # templates/form.html 렌더링


@app.post("/predict")
# /predict 엔드포인트, 이미지 파일을 업로드 받는 API
async def predict(file: UploadFile = File(...)):
    # 1️⃣ 요청 로그
    logger.info(
        f"REQUEST | filename={file.filename} content_type={file.content_type}"
    )

    # 이미지 아니면 바로 차단
    if not file.content_type or not file.content_type.startswith("image/"):
        logger.warning(
            f"INVALID_FILE | filename={file.filename} content_type={file.content_type}"
        )
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")

    try:
        # 2️⃣ 이미지 로드
        img_bytes = await file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    except Exception as e:
        logger.exception(
            f"IMAGE_LOAD_FAIL | filename={file.filename} error={str(e)}"
        )
        raise HTTPException(status_code=400, detail="이미지 로딩에 실패했습니다.")

    # 3️⃣ YOLO 추론 + 시간 측정
    start = time.time()
    results = model(img)
    elapsed = time.time() - start

    r = results[0]
    boxes = r.boxes

    draw = ImageDraw.Draw(img)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_filename = f"{timestamp}_{file.filename}"

    # 4️⃣ 탐지 실패 처리
    if boxes is None or len(boxes) == 0:
        logger.info(
            f"RESULT | filename={file.filename} status=FAIL inference_time={elapsed:.3f}s"
        )

        # 실패 문구 표시
        draw.text(
            (20, 20),
            "Prediction Failed: No object detected",
            fill="red"
        )

        save_path = OUTPUT_DIR / f"failed_{save_filename}"
        img.save(save_path)

    # 5️⃣ 탐지 성공 처리
    else:
        xyxy = boxes.xyxy.cpu().numpy()
        conf = boxes.conf.cpu().numpy()
        cls = boxes.cls.cpu().numpy()
        names = r.names

        for (x1, y1, x2, y2), c, k in zip(xyxy, conf, cls):
            k = int(k)
            label = f"{names.get(k, k)} {c:.2f}"

            # bbox
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

            # 텍스트 크기
            bbox_text = draw.textbbox((0, 0), label)
            text_w = bbox_text[2] - bbox_text[0]
            text_h = bbox_text[3] - bbox_text[1]

            # 텍스트 배경
            draw.rectangle(
                [x1, y1 - text_h - 6, x1 + text_w + 6, y1],
                fill="red"
            )
            draw.text((x1 + 3, y1 - text_h - 3), label, fill="white")

        logger.info(
            f"RESULT | filename={file.filename} status=SUCCESS "
            f"boxes={len(boxes)} inference_time={elapsed:.3f}s"
        )

        save_path = OUTPUT_DIR / f"success_{save_filename}"
        img.save(save_path)

    # 6️⃣ 응답용 이미지 (메모리)
    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="image/png",
        headers={
            "Content-Disposition": f"inline; filename=result_{file.filename}"
        }
    )

# uvicorn src.api.main:app --reload