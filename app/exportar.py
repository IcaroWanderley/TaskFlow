# app/exportar.py

# Importa a classe GerenciadorTarefas do módulo gerenciador
from gerenciador import GerenciadorTarefas

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    # Inicializa o gerenciador de tarefas
    gerenciador = GerenciadorTarefas()
    
    # Exporta as tarefas para um arquivo JSON
    gerenciador.exportar_tarefas_json()
    
    # Imprime uma mensagem indicando que a exportação foi concluída
    print("Exportação concluída! Verifique o arquivo tasks.json.")