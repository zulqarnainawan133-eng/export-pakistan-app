import uvicorn
import sys
import os

# Add the current directory to sys.path so 'app' can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    print("Starting Farmer Trade-Tech Platform Backend...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
