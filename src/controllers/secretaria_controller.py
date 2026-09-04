from fastapi import APIRouter, HTTPException, status

from src.repositories import secretaria_repository
from src.schemas.secretaria_schema import SecretariaCadastro, SecretariaEditar
from src.validation import validate_secretaria

router = APIRouter()

@router.get("/secretarias")
def listar_secretarias():
    return secretaria_repository.consultar_todos()

@router.post("/secretarias")
def cadastrar_secretaria(secretaria: SecretariaCadastro):
    validate_secretaria(secretaria)
    secretaria_criada = secretaria_repository.cadastrar(secretaria)
    return secretaria_criada

@router.delete("/secretarias/{id}")
def apagar(id: int):
    secretaria_repository.apagar(id)
    return {"status": "OK"}

@router.get("/secretarias/{id}")
def consultar_por_id(id: int):
    secretaria = secretaria_repository.consultar_por_id(id)

    if secretaria is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Secretaria não encontrada"
        )

    return secretaria


@router.put("/secretarias/{id}")
def editar(id: int, secretaria: SecretariaEditar):
    secretaria_existente = secretaria_repository.consultar_por_id(id)

    if secretaria_existente is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Secretaria não encontrada"
    )

    validate_secretaria(secretaria)

    secretaria_repository.editar(id, secretaria)
    return {"status": "OK"}
