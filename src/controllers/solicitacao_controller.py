from fastapi import APIRouter, HTTPException, status

from src.repositories import solicitacao_repository
from src.schemas.solicitacao import SolicitacaoCadastro, SolicitacaoEditar


router = APIRouter()

@router.get("/solicitacao")
def listar_solicitacoes():
    return solicitacao_repository.consultar_todos()


@router.post("/solicitacao")
def cadastrar_solicitacao(solicitacao: SolicitacaoCadastro):
    solicitacao_criada = solicitacao_repository.cadastrar(solicitacao)
    return solicitacao_criada


@router.delete("/solicitacao/{id}")
def apagar(id: int):
    solicitacao_repository.apagar(id)
    return {"status": "OK"}


@router.put("/solicitacao/{id}")
def editar(id: int, solicitacao: SolicitacaoEditar):
    solicitacao_existente = solicitacao_repository.consultar_por_id(id)

    if solicitacao_existente is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )

    solicitacao_repository.editar(id, solicitacao)
    return {"status": "OK"}


@router.get("/solicitacao/{id}")
def consultar_por_id(id: int):
    solicitacao = solicitacao_repository.consultar_por_id(id)

    if solicitacao is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    return solicitacao