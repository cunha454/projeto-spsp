from typing import Optional

from src.database.conexao import conectar
from src.schemas.solicitacao import Solicitacao, SolicitacaoCadastro, SolicitacaoEditar


def consultar_todos() -> list[Solicitacao]:
    sql = """
        SELECT
            id,
            descricao,
            data_solicitacao,
            status,
            id_endereco,
            id_servico,
            id_funcionario
        FROM solicitacao
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            registros = cursor.fetchall()

    solicitacoes: list[Solicitacao] = []

    for registro in registros:
        solicitacao = Solicitacao(
            id=registro[0],
            descricao=registro[1],
            data_solicitacao=registro[2],
            status=registro[3],
            id_endereco=registro[4],
            id_servico=registro[5],
            id_funcionario=registro[6]
        )
        solicitacoes.append(solicitacao)

    return solicitacoes


def cadastrar(solicitacao: SolicitacaoCadastro):
    sql = """
        INSERT INTO solicitacao (
            descricao,
            data_solicitacao,
            status,
            id_endereco,
            id_servico,
            id_funcionario
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    solicitacao.descricao,
                    solicitacao.data_solicitacao,
                    solicitacao.status,
                    solicitacao.id_endereco,
                    solicitacao.id_servico,
                    solicitacao.id_funcionario
                )
            )
            conexao.commit()
            novo_id = cursor.lastrowid

    return Solicitacao(
        id=novo_id,
        descricao=solicitacao.descricao,
        data_solicitacao=solicitacao.data_solicitacao,
        status=solicitacao.status,
        id_endereco=solicitacao.id_endereco,
        id_servico=solicitacao.id_servico,
        id_funcionario=solicitacao.id_funcionario
    )


def apagar(id: int):
    sql = "DELETE FROM solicitacao WHERE id = %s"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            conexao.commit()


def editar(id: int, solicitacao: SolicitacaoEditar):
    sql = """
        UPDATE solicitacao SET
            descricao = %s,
            data_solicitacao = %s,
            status = %s,
            id_endereco = %s,
            id_servico = %s,
            id_funcionario = %s
        WHERE id = %s
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    solicitacao.descricao,
                    solicitacao.data_solicitacao,
                    solicitacao.status,
                    solicitacao.id_endereco,
                    solicitacao.id_servico,
                    solicitacao.id_funcionario,
                    id
                )
            )
            conexao.commit()


def consultar_por_id(id: int) -> Optional[Solicitacao]:
    sql = """
        SELECT
            id,
            descricao,
            data_solicitacao,
            status,
            id_endereco,
            id_servico,
            id_funcionario
        FROM solicitacao
        WHERE id = %s
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()

    if registro is None:
        return None

    return Solicitacao(
        id=registro[0],
        descricao=registro[1],
        data_solicitacao=registro[2],
        status=registro[3],
        id_endereco=registro[4],
        id_servico=registro[5],
        id_funcionario=registro[6]
    )
