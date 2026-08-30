from dataclasses import dataclass

@dataclass
class Funcionario:
    id: int
    nome: str
    cargo: str
    telefone: str
    email: str
    id_secretaria: int

@dataclass
class FuncionarioCadastro:
    nome: str
    cargo: str
    telefone: str
    email: str
    id_secretaria: int

@dataclass
class FuncionarioEditar:
    nome: str
    cargo: str
    telefone: str
    email: str
    id_secretaria: int
