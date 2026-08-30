from fastapi import APIRouter, HTTPException, status

from src.repositories import servico_repository
from src.schemas.servico import ServicoCadastro, ServicoEditar

router = APIRouter()

@router.get("/servico")
def listar_servicos():
    return servico_repository.consultar_todos()

@router.post("/servico")
def cadastrar_servico(servico: ServicoCadastro):
    servico_criado = servico_repository.cadastrar(servico)
    return servico_criado

@router.delete("/servico/{id}")
def apagar(id: int):
    servico_repository.apagar(id)
    return {"status": "OK"}

@router.get("/servico/{id}")
def consultar_por_id(id: int):
    servico = servico_repository.consultar_por_id(id)

    if servico is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )

    return servico

@router.put("/servico/{id}")
def editar(id: int, servico: ServicoEditar):
    servico_existente = servico_repository.consultar_por_id(id)

    if servico_existente is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )

    servico_repository.editar(id, servico)
    return {"status": "OK"}
