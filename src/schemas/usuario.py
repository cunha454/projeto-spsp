from dataclasses import dataclass

@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    telefone: int
    data_nascimento: str   