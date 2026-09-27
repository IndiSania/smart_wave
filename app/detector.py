from io import BytesIO
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO


CATEGORY_MAP = {
    "bottle": ("Anorganik", "Masukkan ke tempat sampah anorganik dan pertimbangkan daur ulang."),
    "cup": ("Anorganik", "Pisahkan dari sisa cairan lalu masukkan ke kategori anorganik."),
    "wine glass": ("Anorganik", "Pisahkan sebagai kaca dan tangani dengan hati-hati."),
    "bowl": ("Anorganik", "Periksa materialnya; benda plastik/keramik perlu dipisahkan sesuai fasilitas setempat."),
    "banana": ("Organik", "Dapat dipisahkan sebagai sampah organik untuk kompos."),
    "apple": ("Organik", "Dapat dipisahkan sebagai sampah organik untuk kompos."),
    "orange": ("Organik", "Dapat dipisahkan sebagai sampah organik untuk kompos."),
    "sandwich": ("Organik", "Pisahkan sisa makanan sebagai sampah organik."),
    "carrot": ("Organik", "Dapat dipisahkan sebagai sampah organik untuk kompos."),
    "broccoli": ("Organik", "Dapat dipisahkan sebagai sampah organik untuk kompos."),
    "hot dog": ("Organik", "Pisahkan sisa makanan sebagai sampah organik."),
    "pizza": ("Organik", "Pisahkan sisa makanan sebagai sampah organik."),
    "donut": ("Organik", "Pisahkan sisa makanan sebagai sampah organik."),
    "cake": ("Organik", "Pisahkan sisa makanan sebagai sampah organik."),
    "book": ("Kertas", "Pisahkan dari bahan basah dan masukkan ke pengumpulan kertas jika tersedia."),
    "paper": ("Kertas", "Pisahkan dari bahan basah dan masukkan ke pengumpulan kertas."),
    "cardboard": ("Kertas", "Lipat dan pisahkan dari sampah basah untuk didaur ulang."),
    "cell phone": ("Elektronik", "Jangan dibuang bersama sampah rumah tangga; gunakan titik pengumpulan e-waste."),
    "laptop": ("Elektronik", "Gunakan fasilitas pengelolaan limbah elektronik."),
    "keyboard": ("Elektronik", "Gunakan fasilitas pengelolaan limbah elektronik."),
    "mouse": ("Elektronik", "Gunakan fasilitas pengelolaan limbah elektronik."),
}

DEFAULT_CATEGORY = (
    "Lainnya",
    "Periksa material objek dan ikuti aturan pemilahan sampah di lingkungan setempat.",
)


class WasteDetector:
    def __init__(self, model_path="models/yolo11n.pt"):
        self.model_path = Path(model_path)
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        # Ultralytics will download the model automatically on first run if absent.
        self.model = YOLO(str(self.model_path))

    def predict(self, image_file, confidence=0.35):
        image = Image.open(image_file).convert("RGB")
        frame = np.array(image)

        results = self.model.predict(
            source=frame,
            conf=confidence,
            verbose=False,
        )

        detections = []
        annotated = frame.copy()

        if results:
            result = results[0]
            names = result.names

            if result.boxes is not None:
                for box in result.boxes:
                    cls_id = int(box.cls[0].item())
                    score = float(box.conf[0].item())
                    label = names.get(cls_id, str(cls_id))

                    category, recommendation = CATEGORY_MAP.get(
                        label.lower(), DEFAULT_CATEGORY
                    )

                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    cv2.rectangle(
                        annotated,
                        (x1, y1),
                        (x2, y2),
                        (34, 197, 94),
                        2,
                    )
                    text = f"{label} {score:.0%}"
                    cv2.putText(
                        annotated,
                        text,
                        (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (34, 197, 94),
                        2,
                        cv2.LINE_AA,
                    )

                    detections.append({
                        "label": label,
                        "category": category,
                        "confidence": score,
                        "recommendation": recommendation,
                    })

        return {
            "detections": detections,
            "count": len(detections),
            "summary": self._summary(detections),
            "annotated_image": annotated if detections else None,
        }

    @staticmethod
    def _summary(detections):
        if not detections:
            return "Tidak ada objek terdeteksi"
        categories = sorted(set(d["category"] for d in detections))
        return f"{len(detections)} objek · {', '.join(categories)}"
