from typing import Optional

from src.database.conexao import conectar
from src.schemas.usuario import Usuario



def consultar_todos() -> list[Usuario]:
    """Responsável por consultar todos os clientes"""

    sql = """SELECT
    usuario.id
    usuario.nome
    usuario.email
    usuario.telefone
    usuario.data_nascimento
    FROM usuario
"""
    with conectar() as conexao:
        cursor.execute(sql)
        registros = cursor.fetchall()