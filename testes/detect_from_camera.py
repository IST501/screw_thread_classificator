import cv2
from ultralytics import YOLO


def detect_from_camera(model_path, camera_index=1, conf_threshold=0.25):
    """
    Detect holes and threads in real-time using a connected camera and custom YOLOv8 model.

    Args:
        model_path (str): Path to the trained model (.pt file)
        camera_index (int): Index of the camera to use (0 for built-in, 1 for USB camera)
        conf_threshold (float): Confidence threshold for detections
    """
    # Load the custom model
    model = YOLO(model_path)

    # Open the camera
    cap = cv2.VideoCapture(camera_index)

    while True:
        # Capture a frame from the camera
        success, frame = cap.read()

        if not success:
            break

        # Run inference on the frame
        results = model(frame, conf=conf_threshold)[0]

        # Draw the detections on the frame
        annotated_frame = results.plot()

        # Display the frame
        cv2.imshow("YOLOv8 Detection", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Update this path to match your model file
    MODEL_PATH = "best.pt"

    # Run the detection on the USB camera (camera_index=1)
    detect_from_camera(MODEL_PATH, camera_index=0)
