from fastapi import FastAPI

from apps.projconf.proj_description import description

app = FastAPI(
    title="CardKeeperApi",
    description=description,
    version="1.0.0",
    contact={
        "name": "Alaru",
        # "url": "http://x-force.example.com/contact/",
        "email": "pobrom@gamil.com",
    },
)
