import cv2

# Replace 'your_stream_url' with the actual URL of your ESP32-CAM video stream
stream_url = 'http://192.168.43.79:81/stream'

cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Process the frame (resize, normalize, etc.) as needed
    # ...

    # Perform YOLOv8 object detection on the processed frame
    # ...

    # Display the frame or do further processing
    cv2.imshow('ESP32-CAM Stream', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
