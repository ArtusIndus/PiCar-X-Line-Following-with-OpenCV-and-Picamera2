from picarx import Picarx
from picamera2 import Picamera2
import cv2
import numpy as np
import time

# ============================================================
# Configuration
# ============================================================

SPEED = 5                  # Forward driving speed
CAMERA_TILT = -25          # Camera tilt angle
THRESHOLD = 180            # Binary threshold value
MAX_STEERING_ANGLE = 30    # Maximum steering angle
STEERING_GAIN = 0.1        # Steering sensitivity

# ============================================================
# Hardware Initialization
# ============================================================

px = Picarx()

# Tilt camera downwards to view the track
px.set_cam_tilt_angle(CAMERA_TILT)

# Initialize camera
picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={
            "format": "RGB888",
            "size": (640, 480)
        }
    )
)

picam2.start()

# Allow camera to warm up
time.sleep(2)

# ============================================================
# Main Loop
# ============================================================

try:
    while True:

        # Capture image from camera
        frame = picam2.capture_array()

        # Convert image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Convert grayscale image to binary image
        _, binary = cv2.threshold(
            gray,
            THRESHOLD,
            255,
            cv2.THRESH_BINARY
        )

        height, width = binary.shape

        # Calculate image moments
        moments = cv2.moments(binary)

        if moments["m00"] > 0:

            # Determine center of the detected white area
            cx = int(moments["m10"] / moments["m00"])

            # Calculate deviation from image center
            error = cx - (width // 2)

            # Convert error to steering angle
            steering_angle = np.clip(
                error * STEERING_GAIN,
                -MAX_STEERING_ANGLE,
                MAX_STEERING_ANGLE
            )

            # Apply steering
            px.set_dir_servo_angle(steering_angle)

            # Move forward
            px.forward(SPEED)

            # Draw debug information
            cv2.circle(frame, (cx, height // 2), 8, (0, 0, 255), -1)
            cv2.line(
                frame,
                (width // 2, 0),
                (width // 2, height),
                (255, 0, 0),
                2
            )

            print(
                f"Center X: {cx} | "
                f"Error: {error} | "
                f"Steering: {steering_angle:.1f}"
            )

        else:
            # No line detected
            px.stop()
            print("No line detected.")

        # Show debug windows
        cv2.imshow("Camera Feed", frame)
        cv2.imshow("Binary Image", binary)

        # Exit with Q key
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    # Safe shutdown
    px.stop()
    px.set_dir_servo_angle(0)

    cv2.destroyAllWindows()

    print("Program terminated safely.")
