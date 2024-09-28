from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langfuse.decorators import langfuse_context
import uvicorn

from config import config
from api.router import router
from utils.logger import Loggers

app = FastAPI()
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=True,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






if __name__ == "__main__":
    uvi_cfg = uvicorn.Config(app, host=config.host, port=config.port, workers=config.workers)
    server = uvicorn.Server(uvi_cfg)

    # Use loguru for logging
    Loggers.init_config()

    langfuse_context.configure(
        secret_key=config.langfuse.secret_key,
        public_key=config.langfuse.public_key,
        host=config.langfuse.host,
        enabled=True,
    )

    server.run()

