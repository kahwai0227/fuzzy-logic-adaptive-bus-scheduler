from ultralytics import YOLO

# Load a model
model = YOLO('runs/detect/train8/weights/best.pt')

# Train the model
results = model.train(data='data.yaml', epochs=100, imgsz=640)
