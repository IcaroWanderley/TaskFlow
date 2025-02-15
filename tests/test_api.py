from fastapi.testclient import TestClient
from app.api import app  

# Cria um cliente de teste para a aplicação FastAPI
client = TestClient(app)

# Teste para criar um usuário
def test_create_user():
    # Envia uma requisição POST para criar um novo usuário
    response = client.post(
        "/usuarios/",
        json={"nome": "John Doe", "email": "john@example.com"}
    )
    # Verifica se o status da resposta é 200 (OK)
    assert response.status_code == 200
    # Verifica se a resposta contém um campo "id" não nulo
    assert response.json()["id"] is not None

# Teste para criar uma tarefa
def test_create_task():
    # Primeiro, cria um usuário para associar à tarefa
    user_response = client.post(
        "/usuarios/",
        json={"nome": "Jane Doe", "email": "jane@example.com"}
    )
    # Obtém o ID do usuário criado
    user_id = user_response.json()["id"]

    # Envia uma requisição POST para criar uma nova tarefa associada ao usuário criado
    task_response = client.post(
        "/tarefas/",
        json={
            "titulo": "Nova Tarefa",
            "descricao": "Descrição da tarefa",
            "status": "Pendente",
            "usuario_id": user_id
        }
    )
    # Verifica se o status da resposta é 200 (OK)
    assert task_response.status_code == 200
    # Verifica se a resposta contém um campo "id" não nulo
    assert task_response.json()["id"] is not None