# Copilot Instructions for robo-integracao-geg

## Visão Geral

Este projeto automatiza a autenticação e a extração de relatórios do portal Gente e Gestão, utilizando Python, requests e BeautifulSoup. O fluxo principal está em `src/main.py`, que orquestra login, captura de campos ocultos, envio de payloads e salvamento de respostas HTML.

## Estrutura e Componentes

- `src/main.py`: Script principal. Controla o fluxo de login, manipulação de payloads e requisições HTTP.
- `src/services/login_service.py`: Fornece métodos para:
  - Obter a página de login (`obter_pagina_login`)
  - Capturar campos ocultos do HTML (`capturar_campos_ocultos`)
  - Preparar dados de login (`preparar_dados_login`)
  - Realizar o login (`logar`)
- `src/services/file_service.py`: Utilitário para salvar respostas HTTP em arquivos HTML.
- `src/services/data_service.py`: Gerencia a manipulação de dados e integrações com o banco de dados.
- `src/database/`: Contém scripts para modelagem e manipulação de dados persistentes.
- `output/`: Diretório para logs e arquivos de depuração, como respostas HTML e logs CSV.

## Padrões e Convenções

- **Sessão HTTP**: Sempre reutilize a mesma instância de `requests.Session` para manter cookies e autenticação.
- **Campos Ocultos**: Use `LoginService.capturar_campos_ocultos` para extrair e atualizar dados de formulário entre requisições.
- **Payloads**: O payload do relatório é montado por junção de dicionários (`data | payload`).
- **Headers/Cookies**: Replicados do navegador para simular requests legítimos. Ajuste conforme necessário para evitar bloqueios.
- **Salvamento de Respostas**: Utilize `FileService.save_response_to_file` para registrar respostas relevantes.
- **Logs**: Registre eventos importantes no arquivo `output/automacao.log` para facilitar a depuração.

## Integrações e Dependências

- **Dependências externas**: `requests`, `beautifulsoup4`. Instale via `pip install -r requirements.txt`.
- **Banco de Dados**: Scripts em `src/database/` gerenciam a persistência de dados.
- **Sem framework de testes**: Não há testes automatizados detectados.
- **Sem build system**: O projeto é executado diretamente via `python src/main.py`.

## Fluxo Típico

1. Obter página de login e capturar campos ocultos.
2. Preparar e enviar dados de login.
3. Atualizar campos ocultos após login.
4. Montar e enviar payload para relatório.
5. Salvar respostas HTML para análise.
6. Registrar logs no arquivo `output/automacao.log`.

## Exemplos de Uso

```bash
python src/main.py
```

## Observações

- Ajuste headers/cookies se houver mudanças no portal.
- O código é sensível a mudanças no HTML do portal (campos ocultos, nomes de inputs).
- Não há tratamento de erros robusto; monitore logs e arquivos de saída para depuração.
- Consulte `src/services/` para exemplos de uso dos utilitários e `src/database/` para manipulação de dados persistentes.

---

Adapte este guia conforme o projeto evoluir. Para dúvidas, consulte os arquivos mencionados para exemplos e padrões.
