from fastapi import APIRouter, HTTPException, status

from src.repositories import servico_repository, secretaria_repository
from src.schemas.servico_schema import ServicoCadastro, ServicoEditar
from src.validation import validate_servico, validate_relation

router = APIRouter()

@router.get("/servicos")
def listar_servicos():
    return servico_repository.consultar_todos()

@router.post("/servicos")
def cadastrar_servico(servico: ServicoCadastro):
    validate_servico(servico)
    validate_relation(secretaria_repository, servico.id_secretaria, "secretaria")
    servico_criado = servico_repository.cadastrar(servico)
    return servico_criado

@router.delete("/servicos/{id}")
def apagar(id: int):
    servico_repository.apagar(id)
    return {"status": "OK"}

@router.get("/servicos/{id}")
def consultar_por_id(id: int):
    servico = servico_repository.consultar_por_id(id)

    if servico is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )

    return servico

@router.put("/servicos/{id}")
def editar(id: int, servico: ServicoEditar):
    servico_existente = servico_repository.consultar_por_id(id)

    if servico_existente is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )

    validate_servico(servico)
    validate_relation(secretaria_repository, servico.id_secretaria, "secretaria")

    servico_repository.editar(id, servico)
    return {"status": "OK"}
