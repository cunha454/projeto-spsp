from fastapi import APIRouter, HTTPException, status

from src.repositories import endereco_repository, funcionario_repository, solicitacao_repository, servico_repository
from src.schemas.solicitacao import SolicitacaoCadastro, SolicitacaoEditar
from src.validation import validate_relation, validate_solicitacao

router: APIRouter = APIRouter()


@router.get("/solicitacoes")
def listar_solicitacoes():
    return solicitacao_repository.consultar_todos()


@router.post("/solicitacoes")
def cadastrar_solicitacao(solicitacao: SolicitacaoCadastro):
    validate_solicitacao(solicitacao)
    validate_relation(endereco_repository, solicitacao.id_endereco, "endereço")
    validate_relation(servico_repository, solicitacao.id_servico, "serviço")
    validate_relation(funcionario_repository, solicitacao.id_funcionario, "funcionário")
    return solicitacao_repository.cadastrar(solicitacao)


@router.delete("/solicitacoes/{id}")
def apagar(id: int):
    solicitacao_existente = solicitacao_repository.consultar_por_id(id)

    if solicitacao_existente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada"
        )

    solicitacao_repository.apagar(id)
    return {"status": "OK"}


@router.put("/solicitacoes/{id}")
def editar(id: int, solicitacao: SolicitacaoEditar):
    solicitacao_existente = solicitacao_repository.consultar_por_id(id)

    if solicitacao_existente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada"
        )

    validate_solicitacao(solicitacao)
    validate_relation(endereco_repository, solicitacao.id_endereco, "endereço")
    validate_relation(servico_repository, solicitacao.id_servico, "serviço")
    validate_relation(funcionario_repository, solicitacao.id_funcionario, "funcionário")

    solicitacao_repository.editar(id, solicitacao)
    return {"status": "OK"}


@router.get("/solicitacoes/{id}")
def consultar_por_id(id: int):
    solicitacao = solicitacao_repository.consultar_por_id(id)

    if solicitacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada"
        )

    return solicitacao
