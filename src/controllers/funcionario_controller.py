from fastapi import APIRouter, HTTPException, status

from src.repositories import funcionario_repository
from src.schemas.funcionario import FuncionarioCadastro, FuncionarioEditar

router = APIRouter()

@router.get("/funcionario")
def listar_funcionarios():
    return funcionario_repository.consultar_todos()

@router.post("/funcionario")
def cadastrar_funcionario(funcionario: FuncionarioCadastro):
    funcionario_criado = funcionario_repository.cadastrar(funcionario)
    return funcionario_criado

@router.delete("/funcionario/{id}")
def apagar(id: int):
    funcionario_repository.apagar(id)
    return {"status": "OK"}

@router.get("/funcionario/{id}")
def consultar_por_id(id: int):
    funcionario = funcionario_repository.consultar_por_id(id)

    if funcionario is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    return funcionario

@router.put("/funcionario/{id}")
def editar(id: int, funcionario: FuncionarioEditar):
    funcionario_existente = funcionario_repository.consultar_por_id(id)

    if funcionario_existente is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )

    funcionario_repository.editar(id, funcionario)
    return {"status": "OK"}
