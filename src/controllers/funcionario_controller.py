from fastapi import APIRouter, HTTPException, status

from src.repositories import funcionario_repository, secretaria_repository
from src.schemas.funcionario_schema import FuncionarioCadastro, FuncionarioEditar
from src.validation import validate_funcionario, validate_relation

router = APIRouter()

@router.get("/funcionarios")
def listar_funcionarios():
    return funcionario_repository.consultar_todos()

@router.post("/funcionarios")
def cadastrar_funcionario(funcionario: FuncionarioCadastro):
    validate_funcionario(funcionario)
    validate_relation(secretaria_repository, funcionario.id_secretaria, "secretaria")
    funcionario_criado = funcionario_repository.cadastrar(funcionario)
    return funcionario_criado

@router.delete("/funcionarios/{id}")
def apagar(id: int):
    funcionario_repository.apagar(id)
    return {"status": "OK"}

@router.get("/funcionarios/{id}")
def consultar_por_id(id: int):
    funcionario = funcionario_repository.consultar_por_id(id)

    if funcionario is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    return funcionario

@router.put("/funcionarios/{id}")
def editar(id: int, funcionario: FuncionarioEditar):
    funcionario_existente = funcionario_repository.consultar_por_id(id)

    if funcionario_existente is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )

    validate_funcionario(funcionario)
    validate_relation(secretaria_repository, funcionario.id_secretaria, "secretaria")

    funcionario_repository.editar(id, funcionario)
    return {"status": "OK"}
