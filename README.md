# PiCar-X Line Following with OpenCV and Picamera2

## Overview

This project implements a simple line-following system for the PiCar-X robot using OpenCV and Picamera2. The robot detects a white track in real time and adjusts its steering angle to remain centered on the path.

## Features

* Real-time image processing
* White line detection using thresholding
* Steering control based on image moments
* Adjustable speed and steering sensitivity
* Live camera and binary image debugging
* Safe shutdown handling

## Hardware Requirements

* PiCar-X
* Raspberry Pi
* Raspberry Pi Camera Module
* Power supply

## Software Requirements

* Python 3
* OpenCV
* NumPy
* Picamera2
* PiCar-X Python Library

## Installation

Install the required dependencies:

```bash
pip install opencv-python numpy
```

Ensure that Picamera2 and the PiCar-X library are properly installed on your Raspberry Pi.

## Configuration

The following parameters can be adjusted in the source code:

```python
SPEED = 5
CAMERA_TILT = -25
THRESHOLD = 180
MAX_STEERING_ANGLE = 30
STEERING_GAIN = 0.1
```

## How It Works

1. Capture an image from the camera.
2. Convert the image to grayscale.
3. Apply binary thresholding to isolate the track.
4. Calculate image moments to find the track center.
5. Compute the deviation from the image center.
6. Convert the error into a steering angle.
7. Drive forward while continuously correcting direction.

## Usage

Run the script:

```bash
python line_following.py
```

Press `Q` to exit the program.

## Future Improvements

* Adaptive thresholding
* Region of Interest (ROI) processing
* PID steering controller
* Improved curve detection
* Noise reduction and contour filtering

## License

MIT License

Copyright (c) 2026 ArtusIndus

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.
