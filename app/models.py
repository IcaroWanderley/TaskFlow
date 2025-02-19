from enum import Enum
from pydantic import BaseModel

# Enum para os status das tarefas
class StatusTarefa(str, Enum):
    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDO = "Concluído"

class Usuario:
    def __init__(self, id, nome, email):
        # Inicializa os atributos da classe Usuario
        self.id = id
        self.nome = nome
        self.email = email

    def __repr__(self):
        # Define a representação em string da classe Usuario
        return f"Usuario(id={self.id}, nome={self.nome}, email={self.email})"

class Tarefa:
    def __init__(self, id, titulo, descricao, status: StatusTarefa, usuario_id):
        # Inicializa os atributos da classe Tarefa
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.status = status  # Agora o status é do tipo StatusTarefa
        self.usuario_id = usuario_id

    def __repr__(self):
        # Define a representação em string da classe Tarefa
        return f"Tarefa(id={self.id}, titulo={self.titulo}, descricao={self.descricao}, status={self.status}, usuario_id={self.usuario_id})"

# Modelo Pydantic para a classe Tarefa
class TarefaModel(BaseModel):
    id: int
    titulo: str
    descricao: str
    status: StatusTarefa
    usuario_id: int

    class Config:
        orm_mode = True