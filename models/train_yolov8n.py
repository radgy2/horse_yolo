# !pip install ultralytics pyyaml
import os
import yaml
from pathlib import Path
from ultralytics import YOLO


# =========================
# 1) 경로 설정 (네 프로젝트 기준)
# =========================
PROJECT_ROOT = Path(r"D:\PycharmProjects\horse_yolo_Fastapi")

MODEL_PATH = PROJECT_ROOT / "models" / "yolov8n.pt"
DATA_ROOT = PROJECT_ROOT / "DATA" / "data_yolo"

IMAGES_DIR = DATA_ROOT / "images"
LABELS_DIR = DATA_ROOT / "labels"

NAMES = ["horse"]


# =========================
# 2) 유틸
# =========================
def _assert_dir(p: Path, name: str):
    if not p.exists():
        raise FileNotFoundError(f"[ERROR] {name} 경로가 없습니다: {p}")
    if not p.is_dir():
        raise NotADirectoryError(f"[ERROR] {name} 경로가 폴더가 아닙니다: {p}")


def validate_dataset():
    for split in ["train", "val", "test"]:
        img_dir = IMAGES_DIR / split
        lbl_dir = LABELS_DIR / split

        _assert_dir(img_dir, f"images/{split}")
        _assert_dir(lbl_dir, f"labels/{split}")

        img_files = [
            p for p in img_dir.rglob("*")
            if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        ]

        if not img_files:
            print(f"[WARN] images/{split} 이미지가 없습니다.")
            continue

        missing = 0
        for ip in img_files:
            rel = ip.relative_to(img_dir)
            lp = (lbl_dir / rel).with_suffix(".txt")
            if not lp.exists():
                missing += 1

        if missing > 0:
            print(f"[WARN] {split}: 라벨 없는 이미지 {missing}장")
        else:
            print(f"[OK] {split}: 이미지-라벨 매칭 정상 ({len(img_files)}장)")


def write_data_yaml(path: Path):
    def p(pth: Path) -> str:
        return pth.as_posix()

    data = {
        "train": p(IMAGES_DIR / "train"),
        "val": p(IMAGES_DIR / "val"),
        "test": p(IMAGES_DIR / "test"),
        "nc": len(NAMES),
        "names": NAMES,
    }

    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)

    print(f"[OK] data.yaml 생성 완료 → {path}")


# =========================
# 3) 학습
# =========================
def train():
    _assert_dir(PROJECT_ROOT, "PROJECT_ROOT")
    _assert_dir(DATA_ROOT, "DATA_ROOT")
    _assert_dir(IMAGES_DIR, "images")
    _assert_dir(LABELS_DIR, "labels")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"[ERROR] YOLO 모델 파일 없음: {MODEL_PATH}")

    validate_dataset()

    data_yaml = DATA_ROOT / "data.yaml"
    write_data_yaml(data_yaml)

    model = YOLO(str(MODEL_PATH))

    model.train(
        data=str(data_yaml),
        epochs=50,
        imgsz=640,
        batch=8,          # CPU 안정값
        workers=2,        # Windows + CPU 최적
        device="cpu",
        project=str(DATA_ROOT / "runs"),
        name="yolo8v_train_result",
        exist_ok=True,
    )

    print("🎉 CPU 학습 완료")

train()
