import pytest
from app.gerenciador import GerenciadorTarefas
from app.models import Tarefa, StatusTarefa

@pytest.fixture
def gerenciador():
    return GerenciadorTarefas()

def test_cadastrar_tarefa(gerenciador):
    # Cadastra um usuário para associar à tarefa
    usuario_id = gerenciador.cadastrar_usuario("Ana Costa", "ana.costa@example.com")
    
    # Testa o cadastro de uma nova tarefa
    tarefa_id = gerenciador.cadastrar_tarefa("Implementar login", "Criar sistema de autenticação", StatusTarefa.PENDENTE, usuario_id)
    assert tarefa_id is not None

def test_listar_tarefas(gerenciador):
    # Cadastra um usuário e uma tarefa
    usuario_id = gerenciador.cadastrar_usuario("Pedro Alves", "pedro.alves@example.com")
    gerenciador.cadastrar_tarefa("Criar documentação", "Documentar o sistema", StatusTarefa.EM_ANDAMENTO, usuario_id)
    
    # Testa a listagem de tarefas
    tarefas = gerenciador.listar_tarefas()
    assert len(tarefas) > 0
    assert isinstance(tarefas[0], Tarefa)

def test_listar_tarefas_por_usuario(gerenciador):
    # Cadastra um usuário e uma tarefa
    usuario_id = gerenciador.cadastrar_usuario("Luiza Mendes", "luiza.mendes@example.com")
    gerenciador.cadastrar_tarefa("Testar API", "Escrever testes para a API", StatusTarefa.CONCLUIDO, usuario_id)
    
    # Testa a listagem de tarefas por usuário
    tarefas = gerenciador.listar_tarefas_por_usuario(usuario_id)
    assert len(tarefas) > 0
    assert tarefas[0].usuario_id == usuario_id