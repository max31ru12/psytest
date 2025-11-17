
import sys
import uvicorn
from main import app


def is_frozen() -> bool:
    return getattr(sys, "frozen", False)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        # reload=not is_frozen()
    )
