from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO('runs/detect/train11/weights/last.pt')

count = 0

# Run inference on the source
results = model(source="http://192.168.43.79:81/stream", conf=0.6, stream=True, show=True)  # list of Results objects

for result in results:
    f = open("count.txt", 'w')
    count = result.__len__()
    f.write(str(count))
    f.close()

