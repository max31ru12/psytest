
import sys
import uvicorn
from main import app


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        # workers=4,
        # reload=False,
    )
