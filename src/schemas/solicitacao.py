from dataclasses import dataclass

@dataclass
class Solicitacao:
    id: int
    descricao: str
    data_solicitacao: str
    status: str
    id_endereco: int
    id_servico: int
    id_funcionario: int


@dataclass
class SolicitacaoCadastro:
    descricao: str
    data_solicitacao: str
    status: str
    id_endereco: int
    id_servico: int
    id_funcionario: int


@dataclass
class SolicitacaoEditar:
    descricao: str
    data_solicitacao: str
    status: str
    id_endereco: int
    id_servico: int
    id_funcionario: int
