from dataclasses import dataclass

from src.schemas.endereco import Endereco
# CREATE TABLE solicitacao (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     descricao VARCHAR(255) NOT NULL,
#     data_solicitacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     status VARCHAR(30) NOT NULL DEFAULT 'Pendente',
#     id_endereco INT NOT NULL,
#     id_servico INT NOT NULL,
#     id_funcionario INT NOT NULL,
#     FOREIGN KEY (id_endereco) REFERENCES endereco(id),
#     FOREIGN KEY (id_servico) REFERENCES servico(id),
#     FOREIGN KEY (id_funcionario) REFERENCES funcionario(id)
# )




@dataclass
class Solicitacao:
    id: int
    descricao: str
    data_solicitacao: str
    status: str
    # endereco: Endereco
    # servico:  Servico
    # funcionario: Funcionario


