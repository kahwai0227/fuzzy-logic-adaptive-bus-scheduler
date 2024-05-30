from ultralytics import YOLO

model = YOLO('runs/detect/train11/weights/last.pt')

image_path = ['test_images/img1.jpg', 'test_images/img2.jpeg', 'test_images/img3.jpeg']

results = model(image_path)  # return a list of Results objects

# Process results list
for result in results:
    n=0
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    result.save(filename=("result" + str(n) + ".jpg"))  # save to disk
    n = n + 1
