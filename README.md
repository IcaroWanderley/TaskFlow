# TaskFlow

TaskFlow é uma API de gerenciamento de tarefas construída com FastAPI e MySQL. Ela permite que os usuários gerenciem tarefas e usuários, fornecendo endpoints para criar, listar, atualizar e excluir tarefas e usuários. O projeto é containerizado usando Docker e Docker Compose.

## Funcionalidades

- Criar, listar, atualizar e excluir usuários
- Criar, listar, atualizar e excluir tarefas
- Exportar tarefas para um arquivo JSON
- Documentação interativa da API com Swagger UI

## Requisitos

- Docker
- Docker Compose

## Configuração

1. Clone o repositório:

   ```bash
   git clone https://github.com/seuusuario/taskflow.git
   cd taskflow

2. Construa e inicie os containers Docker:

    docker-compose up --build

3. Documentação do FastAPI, onde são encontradas os testes:

    http://localhost:8000/docs