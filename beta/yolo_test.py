from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.train(
    data="coco128.yaml", epochs=3, batch_size=16, weights="yolov8n.pt", device="cpu"
)
results = model("./known_faces/midhun.jpg")

print(results)
