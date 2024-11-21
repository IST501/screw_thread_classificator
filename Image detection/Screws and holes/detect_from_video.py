from ultralytics import YOLO
import cv2
import time


def process_video(model_path, video_path, conf_threshold=0.39):
    """
    Process video using custom YOLOv8 model to detect holes and threads in gears.

    Args:
        model_path (str): Path to the trained model (.pt file)
        video_path (str): Path to the input video
        conf_threshold (float): Confidence threshold for detections
    """
    # Load the custom model
    model = YOLO(model_path)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Create video writer
    output_path = "output_detection.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Process the video
    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            break

        # Run inference on the frame
        results = model(frame, conf=conf_threshold)[0]

        # Draw the detections on the frame
        annotated_frame = results.plot()

        # Write the frame to output video
        out.write(annotated_frame)

        # Display the frame (optional - comment out if running on server)
        cv2.imshow("YOLOv11 Detection", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Update these paths to match your files
    MODEL_PATH = "100 epochs/best.pt"
    VIDEO_PATH = "Sem_rosca.mp4"

    # Process the video
    process_video(MODEL_PATH, VIDEO_PATH)
