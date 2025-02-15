import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.database import criar_conexao

@pytest.fixture
def client():
    # Cria uma instância do TestClient
    return TestClient(app)

@pytest.fixture(autouse=True)
def limpar_banco_de_dados():
    # Limpa as tabelas antes de cada teste
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM tarefas")
    cursor.execute("DELETE FROM usuarios")
    conexao.commit()
    conexao.close()