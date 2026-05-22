# Farmer Trade-Tech Platform

A trade-tech platform for Pakistani farmers featuring shipment tracking, farmer registration, and RAAST payment integration.

## Backend (FastAPI)

### Prerequisites
- Python 3.10+

### Installation
```bash
pip install -r requirements.txt
```

### Running the Backend
To start the backend server, run the `run.py` script from the root directory:
```bash
python3 run.py
```
The API will be available at http://localhost:8000.
- Root: http://localhost:8000/
- Shipment Tracking: http://localhost:8000/api/v1/track/GD-2023-1234
- Mock PSW API: http://localhost:8000/mock-psw/GD-2023-1234

### Running Tests
```bash
pytest tests/
```

## Frontend (Flutter)

### Prerequisites
- Flutter SDK
- Firebase account (for Auth)

### Installation
```bash
cd frontend
flutter pub get
```

### Running the App
```bash
cd frontend
flutter run -d chrome  # For web
# OR
flutter run            # For mobile/desktop
```

### Running Tests
```bash
cd frontend
flutter test
```

## Project Structure
- `app/`: FastAPI backend source code.
- `frontend/`: Flutter frontend source code.
- `tests/`: Backend unit and integration tests.
- `run.py`: Convenient script to run the backend.
- `requirements.txt`: Python dependencies.
