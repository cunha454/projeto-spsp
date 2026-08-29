from dataclasses import dataclass

@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    telefone: int
    data_nascimento: str   


@dataclass
class UsuarioCadastro:
    id: int
    nome: str
    email: str
    telefone: int
    data_nascimento: str   


@dataclass
class UsuarioEditar:
    id: int
    nome: str
    email: str
    telefone: int
    data_nascimento: str   

#------------------------------------------------------------------------------------------

