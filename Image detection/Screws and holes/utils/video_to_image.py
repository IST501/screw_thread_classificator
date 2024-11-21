import os
from pathlib import Path

import cv2


def extract_frames(video_path, output_folder, frame_interval=10):
    """
    Extract frames from a video at specified intervals.

    Args:
        video_path (str): Path to the input video file
        output_folder (str): Path to save the extracted frames
        frame_interval (int): Extract one frame every N frames
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the video file
    video = cv2.VideoCapture(str(video_path))

    # Get basic video information
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)

    print(f"Total frames: {total_frames}")
    print(f"FPS: {fps}")

    frame_count = 0
    saved_count = 0

    while True:
        success, frame = video.read()

        if not success:
            break

        # Save frame if it's at the specified interval
        if frame_count % frame_interval == 0:
            frame_path = os.path.join(output_folder, f"frame_{frame_count:06d}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_count += 1

        frame_count += 1

        # Print progress
        if frame_count % 100 == 0:
            print(f"Processed {frame_count}/{total_frames} frames")

    # Release video object
    video.release()

    print(f"\nExtraction complete!")
    print(f"Saved {saved_count} frames to {output_folder}")


if __name__ == "__main__":
    # Get the project root directory (Srews folder)
    project_root = Path(__file__).parent.parent

    # Define paths relative to project root
    video_path = project_root / "Data" / "NewPN" / "meioS.mp4"
    output_folder = project_root / "Data" / "NewPN_Images" / "meioS"

    # Convert paths to strings and create frames
    extract_frames(
        video_path=str(video_path), output_folder=str(output_folder), frame_interval=10
    )
