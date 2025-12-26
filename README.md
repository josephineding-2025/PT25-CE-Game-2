# PT25-CE-Game-2 - Motion Detection Game

A fun and interactive motion detection game that uses computer vision to track your poses and gestures. Perform various yoga-inspired poses in front of your webcam to score points and progress through different stages!

## 🎮 Game Features

- **8 Unique Poses**: Master poses like "The Awakening", "The Archer", "Iron Sumo", and more
- **Two-Stage Gameplay**:
  - **Stage 1**: Sequential pose challenges with decreasing time limits
  - **Stage 2**: Random shuffle mode with 3-second time limits
- **Hand Gesture Start**: Show two fists to begin the game
- **Real-time Pose Detection**: Uses MediaPipe for accurate pose tracking
- **Score System**: Earn points by correctly matching poses

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** (Python 3.11 recommended)
- **Webcam** (built-in or external)
- **Windows 10/11** (tested on Windows)

## 🚀 Installation

### Step 1: Clone or Download the Repository

If you haven't already, navigate to the project directory:
```bash
cd PT25-CE-Game-2
```

### Step 2: Create a Virtual Environment (Recommended)

Create a virtual environment to isolate project dependencies:

**On Windows:**
```bash
python -m venv venv
```

**Activate the virtual environment:**

**On Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**On Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

If you encounter execution policy errors in PowerShell, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

**Note:** The `requirements.txt` file may be missing some dependencies. If you encounter import errors, install these additional packages:

```bash
pip install opencv-python mediapipe
```

Or install all dependencies at once:
```bash
pip install -r requirements.txt opencv-python mediapipe
```

### Step 4: Verify Installation

Verify that OpenCV and MediaPipe are installed correctly:
```bash
python -c "import cv2; import mediapipe; print('All dependencies installed successfully!')"
```

## 🎯 How to Run

1. **Activate your virtual environment** (if not already activated):
   ```bash
   venv\Scripts\activate
   ```

2. **Run the game**:
   ```bash
   python backend/main.py
   ```

3. **Start Playing**:
   - Position yourself in front of your webcam
   - Make sure you're well-lit and fully visible
   - Show **two fists** to start the countdown
   - Follow the on-screen instructions to perform the required poses

## 🎮 Game Controls

- **Two Fists Gesture**: Start the game (hold both fists up)
- **'q' Key**: Quit the game
- **'r' Key**: Retry/Reset after game over
- **'f' Key**: Toggle fullscreen mode

## 🧘 Available Poses

1. **The Awakening**: Arms raised overhead, creating a circle 'O' shape
2. **The Archer**: Standing sideways, one arm straight, one bent (drawing bow)
3. **The Iron Sumo**: Wide squat, arms hanging down
4. **Disco Diagonal**: One arm high, one hand on hip
5. **The Golden Rooster**: One leg balance, arms T-pose, hands down
6. **The Shell Defence**: Crouching tight ball
7. **Ninja Ground Tap**: Side lunge, one hand floor, one hand up
8. **Supernova X**: Body extended in X shape

## 📊 Game Mechanics

- **Stage 1**: Complete all 8 poses sequentially
  - Time limit starts at 10 seconds and decreases by 1 second per pose
  - Minimum time limit: 3 seconds
- **Stage 2**: Random pose shuffle mode
  - Fixed 3-second time limit per pose
  - Poses are randomly selected
- **Scoring**: You need a score of 6/10 or higher to pass each pose
- **Game Over**: Occurs when time runs out

## 🛠️ Troubleshooting

### Webcam Not Detected
- Ensure your webcam is connected and not being used by another application
- Try changing the camera index in `main.py` (line 395): `cv2.VideoCapture(1)` instead of `cv2.VideoCapture(0)`

### Import Errors
If you see errors like `ModuleNotFoundError: No module named 'cv2'` or `No module named 'mediapipe'`:
```bash
pip install opencv-python mediapipe
```

### Poor Pose Detection
- Ensure good lighting in your room
- Stand at an appropriate distance from the webcam (2-3 meters)
- Wear contrasting clothing to improve detection
- Make sure your full body is visible in the frame

### Virtual Environment Issues
If activation fails:
- Make sure you're in the project root directory
- Try recreating the virtual environment: `python -m venv venv --clear`

### Performance Issues
- Close other applications using the webcam
- Reduce background processes
- Lower the webcam resolution if needed

## 📁 Project Structure

```
PT25-CE-Game-2/
├── backend/
│   └── main.py          # Main game logic and pose detection
├── venv/                # Virtual environment (gitignored)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Technical Details

- **Computer Vision**: OpenCV for video capture and processing
- **Pose Detection**: MediaPipe Pose for body landmark detection
- **Hand Detection**: MediaPipe Hands for gesture recognition
- **Game Engine**: Custom Python game logic with real-time pose scoring

## 📝 Notes

- The game uses normalized coordinates (0-1) for pose detection
- Pose scoring is based on angle calculations and distance measurements
- The game window can be resized and toggled to fullscreen

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements!

## 📄 License

This project is part of the PT25-CE Game series.

---

**Enjoy the game and have fun mastering all the poses!** 🎉

