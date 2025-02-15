import pytest
from app.gerenciador import GerenciadorTarefas
from app.models import Usuario

@pytest.fixture
def gerenciador():
    return GerenciadorTarefas()

def test_cadastrar_usuario(gerenciador):
    # Testa o cadastro de um novo usuário
    usuario_id = gerenciador.cadastrar_usuario("João Silva", "joao.silva@example.com")
    assert usuario_id is not None

def test_listar_usuarios(gerenciador):
    # Testa a listagem de usuários
    gerenciador.cadastrar_usuario("Maria Oliveira", "maria.oliveira@example.com")
    usuarios = gerenciador.listar_usuarios()
    assert len(usuarios) > 0
    assert isinstance(usuarios[0], Usuario)

def test_cadastrar_usuario_email_duplicado(gerenciador):
    # Testa o cadastro de um usuário com email duplicado
    gerenciador.cadastrar_usuario("Carlos Souza", "carlos.souza@example.com")
    usuario_id = gerenciador.cadastrar_usuario("Carlos Souza", "carlos.souza@example.com")
    assert usuario_id is None