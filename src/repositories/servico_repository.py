from typing import List, Optional

from src.database.conexao import conectar
from src.schemas.servico import Servico, ServicoCadastro, ServicoEditar

def consultar_todos() -> List[Servico]:
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT id, nome, descricao, id_secretaria FROM servico")
            registros = cursor.fetchall()

    servicos: list[Servico] = []
    for registro in registros:
        servico = Servico(
            id=registro[0],
            nome=registro[1],
            descricao=registro[2],
            id_secretaria=registro[3]
        )
        servicos.append(servico)

    return servicos


def cadastrar(servico: ServicoCadastro):
    """Responsável por cadastrar o serviço no banco de dados"""
    sql = "INSERT INTO servico (nome, descricao, id_secretaria) VALUES (%s, %s, %s)"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    servico.nome,
                    servico.descricao,
                    servico.id_secretaria
                )
            )

            novo_id = cursor.lastrowid
            conexao.commit()

    return Servico(
        id=novo_id,
        nome=servico.nome,
        descricao=servico.descricao,
        id_secretaria=servico.id_secretaria
    )

def apagar(id: int):
    """Responsável por apagar o serviço do banco de dados"""
    sql = "DELETE FROM servico WHERE id = %s"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            conexao.commit()


def consultar_por_id(id: int) -> Optional[Servico]:
    """Responsável por consultar o serviço filtrando por id"""
    sql = "SELECT id, nome, descricao, id_secretaria FROM servico WHERE id = %s"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()

    if registro is None:
        return None

    return Servico(
        id=registro[0],
        nome=registro[1],
        descricao=registro[2],
        id_secretaria=registro[3]
    )

def editar(id: int, servico: ServicoEditar):
    """Responsável por alterar os dados do serviço no banco de dados"""
    sql = "UPDATE servico SET nome = %s, descricao = %s, id_secretaria = %s WHERE id = %s"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    servico.nome,
                    servico.descricao,
                    servico.id_secretaria,
                    id
                )
            )
            conexao.commit()
