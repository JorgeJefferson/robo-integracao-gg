# Este módulo contém utilitários para salvar respostas HTTP em arquivos HTML.
import os

def save_response_to_file(response, filename):
    """Salva o conteúdo de uma resposta HTTP em um arquivo."""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.text)

    print(f"Resposta salva em {filename}")
