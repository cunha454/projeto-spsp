from dataclasses import dataclass

@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    telefone: str
    data_nascimento: str   


@dataclass
class UsuarioCadastro:
    nome: str
    email: str
    telefone: str
    data_nascimento: str   


@dataclass
class UsuarioEditar:
    nome: str
    email: str
    telefone: str
    data_nascimento: str   

#------------------------------------------------------------------------------------------
