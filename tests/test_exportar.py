import pytest
import os
from app.gerenciador import GerenciadorTarefas
from app.models import StatusTarefa

@pytest.fixture
def gerenciador():
    return GerenciadorTarefas()

def test_exportar_tarefas_json(gerenciador):
    # Cadastra um usuário e uma tarefa
    usuario_id = gerenciador.cadastrar_usuario("Fernanda Lima", "fernanda.lima@example.com")
    gerenciador.cadastrar_tarefa("Configurar CI/CD", "Configurar pipeline de integração contínua", StatusTarefa.PENDENTE, usuario_id)
    
    # Testa a exportação de tarefas para JSON
    gerenciador.exportar_tarefas_json("test_tasks.json")
    assert os.path.exists("test_tasks.json")
    
    # Limpa o arquivo de teste após o teste
    os.remove("test_tasks.json")