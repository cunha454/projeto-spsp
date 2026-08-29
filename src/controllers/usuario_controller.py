
from fastapi import APIRouter, HTTPException, status


from src.repositories import usuario_repository
from src.schemas.usuario import UsuarioCadastro, UsuarioEditar

router: APIRouter = APIRouter(prefix="/usuario")




@router.get("")
def listar_usuarios():
    return usuario_repository.consultar_todos()


@router.post("")
def cadastrar(usuario: UsuarioCadastro):
    return usuario_repository.cadastrar(usuario)


@router.put("/{id}")
def editar(id: int, usuario: UsuarioEditar):
    usuario_banco = usuario.repository.consultar_por_id(id)

    if usuario_banco is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado")

    usuario.repository.editar(id, usuario)
    return {
        "status": "ok"
    }


@router.delete("/usuario/{id}")
def apagar(id: int):
    usuario_repository.apagar(id)
    # N é a forma final, faremos diferente, falta tratar 404, deve ser um 
    # 204 No content 
    return {"status": "OK"}
