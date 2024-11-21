import cv2
from ultralytics import YOLO


def detect_from_cameras(model_path, camera_indices=[1, 2, 3], conf_threshold=0.4):
    # Load the custom model
    model = YOLO(model_path)

    # Define custom colors for each class
    # BGR format (OpenCV uses BGR, not RGB)
    class_colors = {
        "Com-rosca": (0, 255, 0),  # Green for Com_rosca
        "Sem-rosca": (0, 0, 255),  # Red for Sem_rosca
    }

    # Open the cameras
    caps = [cv2.VideoCapture(idx) for idx in camera_indices]

    # Create windows
    cv2.namedWindow("Camera 1", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Camera 2", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Camera 3", cv2.WINDOW_NORMAL)

    while True:
        # Capture frames from each camera
        success, frames = True, []
        for cap in caps:
            frame_success, frame = cap.read()
            success &= frame_success
            frames.append(frame)

        if not success:
            break

        # Run inference on the frames
        results = [model(frame, conf=conf_threshold)[0] for frame in frames]

        # Draw the best detection on each frame
        for i, res in enumerate(results):
            frame = frames[i].copy()

            # Draw bounding boxes with custom colors
            for box in res.boxes:
                # Get class name
                cls = model.names[int(box.cls[0])]

                # Get color for this class
                color = class_colors.get(
                    cls, (255, 255, 255)
                )  # Default to white if class not found

                # Get box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Get confidence
                conf = float(box.conf[0])

                # Draw rectangle
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                # Put class label and confidence
                label = f"{cls} {conf:.2f}"
                cv2.putText(
                    frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2
                )

            # Display the frame in the corresponding window
            window_name = f"Camera {i+1}"
            cv2.imshow(window_name, frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the cameras and close the windows
    for cap in caps:
        cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Update this path to match your model file
    MODEL_PATH = "Final/best.pt"

    # Run the detection on the 3 cameras
    detect_from_cameras(MODEL_PATH)
