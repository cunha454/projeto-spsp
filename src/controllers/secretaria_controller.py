from fastapi import APIRouter, HTTPException, status

from src.repositories import secretaria_repository
from src.schemas.secretaria import SecretariaCadastro, SecretariaEditar

router = APIRouter()

@router.get("/secretaria")
def listar_secretarias():
    return secretaria_repository.consultar_todos()

@router.post("/secretaria")
def cadastrar_secretaria(secretaria: SecretariaCadastro):
    secretaria_criada = secretaria_repository.cadastrar(secretaria)
    return secretaria_criada

@router.delete("/secretaria/{id}")
def apagar(id: int):
    secretaria_repository.apagar(id)
    return {"status": "OK"}

@router.get("/secretaria/{id}")
def consultar_por_id(id: int):
    secretaria = secretaria_repository.consultar_por_id(id)

    if secretaria is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Secretaria não encontrada"
        )

    return secretaria


@router.put("/secretaria/{id}")
def editar(id: int, secretaria: SecretariaEditar):
    secretaria_existente = secretaria_repository.consultar_por_id(id)

    if secretaria_existente is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Secretaria não encontrada"
    )

    secretaria_repository.editar(id, secretaria)
    return {"status": "OK"}

