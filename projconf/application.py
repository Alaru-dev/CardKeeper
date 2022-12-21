from fastapi import FastAPI

from projconf.proj_description import description

app = FastAPI(
    title="CardKeeperApi",
    description=description,
    version="1.0.0",
    contact={
        "name": "Alaru",
        "email": "pobrom@gamil.com",
    },
)
