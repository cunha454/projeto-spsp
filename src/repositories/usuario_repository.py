from sqlite3 import Cursor
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
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            registros = cursor.fetchall()

    usuarios: list[Usuario] = []
    for registro in registros:
        usuario: Usuario = Usuario(
            id=registro[0],
            nome=registro[1],
            email=registro[2],
            telefone=registro[3],
            data_nascimento=registro[4]
        )

    usuarios.append(usuario)
    return usuarios


