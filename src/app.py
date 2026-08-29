from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys


# Permite rodar com `py src/app.py`: coloca a raiz do projeto no sys.path
# para que os imports `from src import .` funcionem corretamente
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.controllers import usuario_controller

# Swagger => http://localhost:8000/docs

app = FastAPI(
    title="Servico API",
    description="Projeto de serviços",
    version="0.1.0",
)

origins = [
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_controller.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=True)


