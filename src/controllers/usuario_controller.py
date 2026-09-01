
from fastapi import APIRouter, HTTPException, status


from src.repositories import usuario_repository
from src.schemas.usuario import UsuarioCadastro, UsuarioEditar

router: APIRouter = APIRouter()


@router.get("/usuarios")
def listar_usuarios():
    return usuario_repository.consultar_todos()


@router.post("/usuarios")
def cadastrar(usuario: UsuarioCadastro):
    return usuario_repository.cadastrar(usuario)


@router.put("/usuarios/{id}")
def editar(id: int, usuario: UsuarioEditar):
    usuario_banco = usuario_repository.consultar_por_id(id)

    if usuario_banco is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado")

    usuario_repository.editar(id, usuario)
    return {
        "status": "ok"
    }


@router.delete("/usuarios/{id}")
def apagar(id: int):
    usuario_repository.apagar(id)
    return {"status": "OK"}


@router.get("/usuarios/{id}")
def consultar_por_id(id: int):
    usuario = usuario_repository.consultar_por_id(id)

    if usuario is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    return usuario
