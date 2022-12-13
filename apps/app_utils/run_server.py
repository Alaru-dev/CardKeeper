import server_settings as set
import uvicorn

from apps.projconf import app

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=set.Host, port=set.Port, log_level="info", reload=True
    )
