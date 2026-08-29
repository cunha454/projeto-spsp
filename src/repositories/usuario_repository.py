from sqlite3 import Cursor
from typing import Optional

from src.database.conexao import conectar
from src.schemas.usuario import Usuario, UsuarioCadastro, UsuarioEditar



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


def cadastrar(usuario: UsuarioCadastro) -> Usuario:
    sql = """INSERT INTO usuario 
    (nome, email, telefone, data_nascimento)
    VALUES (%s, %s, %s, %s)
    """
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (usuario.nome, usuario.email, usuario.telefone, usuario.data_nascimento))
            novo_id = cursor.lastrowid
            conexao.commit()
    return Usuario(
        id=novo_id,
        nome=usuario.nome,
        email=usuario.email,
        telefone=usuario.telefone,
        data_nascimento=usuario.data_nascimento
    )



def editar(id: int, usuario: UsuarioEditar):
    sql = """UPDATE usuario SET 
        nome=%s,
        email=%s,
        telefone=%s,
        data_nascimento=%s,
    WHERE id=%s
    """
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (
                usuario.nome, 
                usuario.email, 
                usuario.telefone, 
                usuario.data_nascimento, 
                id,
            ))
            conexao.commit()


def consultar_por_id(id: int) -> Optional[Usuario]:
    """Reponsável por consultar o usuário filtrando por id"""
    sql = "SELECT id, nome FROM usuario WHERE id = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
    if registro is None:
        return None
    return Usuario(id=registro[0], nome=registro[1])


def apagar(id: int):
    # Alternativa para n apagar o registro fisicamente
    # Desativar o registro, atualizando o registro_ativo
    sql = "UPDATE usuario SET registro_ativo = 0 WHERE id = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            conexao.commit()