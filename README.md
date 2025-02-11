# Hand Gesture Block Drag and Drop

A Python application that uses computer vision and hand gesture recognition to create an interactive block dragging system using your webcam.

## Features

- Real-time hand tracking using MediaPipe
- Interactive blocks that can be dragged using pinch gestures
- FPS display
- Webcam feed with visual feedback for finger positions
- Four draggable blocks

## Prerequisites

Before running this project, make sure you have Python installed on your system. The following libraries are required:

2. Once running:
- You will see your webcam feed with four black squares
- Your index finger will be marked with a blue dot
- Your thumb will be marked with a green dot
- Bring your thumb and index finger close together (pinching gesture) while hovering over a block to drag it
- Press 'q' to quit the program

## Controls

- **Drag**: Pinch your thumb and index finger together while hovering over a block
- **Release**: Spread your fingers apart
- **Exit**: Press 'q' key

## Troubleshooting

If you encounter any issues:
1. Ensure your webcam is properly connected and not in use by other applications
2. Check that you have sufficient lighting for hand detection
3. Verify all required libraries are installed correctly
4. Make sure you have appropriate permissions to access your webcam

## System Requirements

- Python 3.7 or higher
- Webcam
- Sufficient lighting for hand detection
- Minimum 4GB RAM recommended

## Notes

- The program is set to detect only one hand at a time
- Adjust `cam_width` and `cam_height` in the code if needed to match your webcam's resolution
- The grab threshold can be adjusted by modifying the `grab_threshold` value in the `BlockDragDrop` class

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to fork this project and submit pull requests for any improvements.
