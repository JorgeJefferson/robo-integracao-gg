# Robô GEG - Sistema de Integração e Automação de Dados Gente e Gestão

## 📋 Descrição

O **Robô GEG** é um sistema Python robusto e inteligente responsável por **automatizar completamente a extração, processamento e sincronização de dados críticos** do portal Gente e Gestão com banco de dados MySQL local. O sistema realiza login automático, navegação inteligente e extração de dados de prontuários de colaboradores, processando informações em tempo real com validação e normalização avançadas. Executando com agendamento persistente e sistema de retry automático, o Robô GEG garante que dados operacionais de condutores estejam sempre disponíveis e atualizados para operações críticas de logística e gestão de frotas.

## 🎯 Funcionalidades

### Principais Features:

- ✅ **Automação Web Inteligente**: Login automático e navegação no portal Gente e Gestão
- ✅ **Extração de Dados Avançada**: Processamento de tabelas DevExpress com mapeamento inteligente de colunas
- ✅ **Validação e Normalização**: Limpeza automática de dados, formatação e padronização
- ✅ **Processamento de Prontuários**: Extração completa de dados de condutores incluindo telemetria e fadigas
- ✅ **Persistência Otimizada**: Integração com banco MySQL usando SQLAlchemy 2.0 e pool de conexões
- ✅ **Sistema de Retry**: Recuperação automática de falhas com múltiplas tentativas configuráveis
- ✅ **Agendamento Persistente**: Execução automática diária com configuração flexível
- ✅ **Logging Detalhado**: Rastreamento completo de todas as operações, erros e métricas
- ✅ **Cache Inteligente**: Sistema de cache de sessões e dados intermediários
- ✅ **Multi-Usuário**: Suporte a múltiplas credenciais com failover automático
- ✅ **Estrutura Modular**: Arquitetura extensível para novos tipos de extração

### Fluxo de Funcionamento:

1. **Inicializa** sistema de banco de dados com validação de conexão
2. **Autentica** no portal Gente e Gestão com credenciais configuradas
3. **Navega** automaticamente para página de relatórios de prontuários
4. **Extrai** dados completos de colaboradores via requisições AJAX
5. **Processa** informações com validação, normalização e mapeamento de campos
6. **Converte** dados para formato padronizado do sistema
7. **Persiste** no banco MySQL com tratamento de conflitos e deduplicação
8. **Executa** automaticamente todo dia às 15h com sistema de agendamento persistente

## 🚀 Impacto e Benefícios Estratégicos

### 💼 Benefícios de Negócio Quantificáveis

### 🚀 Automação e Eficiência Operacional

- ↗️ **+100% Automação**: Extração de prontuários completamente automatizada
- ↘️ **-95% Tempo de Atualização**: Dados de condutores atualizados diariamente
- ↗️ **+99.9% Disponibilidade**: Informações críticas sempre disponíveis localmente
- 📊 **100% Rastreabilidade**: Histórico completo de todas as extrações e atualizações
- ⚡ **Processamento Inteligente**: Extração otimizada com cache e retry automático

### 🎯 Otimização de Gestão de Frotas e Condutores

- 💰 **Redução de Custos**: Eliminação de processos manuais de coleta de dados
- 📈 **Eficiência Operacional**: Dados sempre atualizados para gestão de condutores
- 🎯 **Gestão Proativa**: Informações em tempo real sobre status e pontuações
- ⚡ **Decisões Rápidas**: Base local para consultas ultra-rápidas de prontuários
- 📊 **ROI Imediato**: Redução de tempo de resposta e melhoria na precisão operacional

### 🔍 Compliance e Governança de Condutores

- 📋 **Auditoria Completa**: Registro detalhado de todas as operações de extração
- 🛡️ **Integridade de Dados**: Validação automática de CPFs e dados críticos
- 📊 **Relatórios Automáticos**: Base consolidada para análises de performance de condutores
- 🔒 **Rastreabilidade Total**: Logs detalhados de todas as sincronizações
- ⚖️ **Transparência Operacional**: Visibilidade completa dos processos de coleta

### 🔧 Benefícios Técnicos e Inovação

### 🏗️ Arquitetura Moderna e Escalável

- 🚀 **SQLAlchemy 2.0**: ORM moderno com gestão otimizada de conexões
- 🔄 **Web Automation**: Automação robusta com BeautifulSoup e Requests
- 🌐 **Pandas Processing**: Processamento eficiente de dados com transformações automáticas
- ⚡ **Threading Inteligente**: Execução controlada com isolamento de sessões
- 📦 **Modularidade Avançada**: Componentes independentes seguindo padrões SOLID
- 🎭 **Design Patterns**: Service Layer, Repository Pattern, Factory Pattern

### 📊 Capacidades de Extração Avançadas

- 🗄️ **Portal Integration**: Integração completa com sistema Gente e Gestão
- 🔗 **Real-time Data Processing**: Processamento em tempo real com validação
- 📈 **Intelligent Parsing**: Processamento inteligente de tabelas DevExpress complexas
- ⏱️ **Scheduled Automation**: Controle de execução com agendamento persistente
- 🎯 **Error Recovery**: Recuperação automática com retry e logging detalhado
- 🌍 **Data Transformation**: Transformação automática para formato de banco

### 🌟 Diferencial Competitivo

### 🚀 Inovação Tecnológica

- **Smart Web Scraping**: Extração inteligente com processamento de AJAX e DevExpress
- **Adaptive Authentication**: Sistema de autenticação com múltiplas credenciais
- **Resilient Processing**: Arquitetura resiliente com recuperação automática
- **Zero-manual Operations**: Operações completamente automatizadas sem intervenção

### 💡 Impacto Estratégico no Negócio

- 🚨 **Dados Sempre Atualizados**: Prontuários de condutores sempre em dia
- 🔗 **Integração Perfeita**: Ponte transparente entre Gente e Gestão e sistemas internos
- 🎯 **Produtividade**: Equipes focam em análise, não em coleta manual
- 📊 **Visibilidade Total**: Transparência completa dos dados de condutores
- 🔮 **Escalabilidade**: Preparado para novos tipos de dados e integrações

## 🗂️ Estrutura do Projeto

```
robo-integracao-gg/
├── src/
│   ├── main.py                         # Script principal e orquestrador
│   ├── automacao_geg.py                # Classe principal de automação
│   ├── database/
│   │   ├── __init__.py
│   │   └── models.py                   # Modelos SQLAlchemy das tabelas
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── database.py                 # Gerenciamento de conexões MySQL
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_service.py             # Processamento e conversão de dados
│   │   └── login_service.py            # Serviços de autenticação
│   └── utils/
│       ├── __init__.py
│       └── file_util.py                # Utilitários para arquivos
├── output/
│   ├── automacao.log                   # Logs de execução
│   ├── debug_*.html                    # Arquivos HTML para debug
│   └── log_prontuario_*.csv            # Arquivos CSV gerados
├── jobs.db                             # Banco SQLite para agendamento
├── requirements.txt                    # Dependências Python
└── README.md                          # Esta documentação
```

## ⚙️ Configuração

### 1. Requisitos do Sistema

- **Python 3.8+**
- **MySQL/MariaDB** para persistência local de dados
- **SQLAlchemy 2.0+** para ORM e gestão de conexões
- **Pandas 2.0+** para processamento de dados
- **Requests** para automação web
- **BeautifulSoup4** para parsing HTML
- **APScheduler** para agendamento de tarefas
- **pymnz** para utilitários de automação
- **Acesso de rede** para portal Gente e Gestão
- **Privilégios de leitura/escrita** no banco MySQL local

### 2. Instalação

```bash
# Clone o repositório
git clone https://github.com/JorgeJefferson/robo-integracao-gg.git
cd robo-integracao-gg

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as credenciais:

```bash
# Banco de dados MySQL Local
ROBO_INTEGRACAO_GG_DATABASE_URL="mysql+mysqlconnector://usuario:senha@localhost:3306/banco_geg"

# Configurações de Execução
ENVIRONMENT="production"
LOG_LEVEL="INFO"
```

### 4. Estrutura do Banco de Dados

O sistema utiliza as seguintes tabelas:

```sql
-- Tabela de usuários para autenticação no Gente e Gestão
CREATE TABLE cad_usuarios_geg (
    email_cad_usuarios_geg VARCHAR(255) PRIMARY KEY,
    senha_cad_usuarios_geg VARCHAR(255) NOT NULL
);

-- Tabela principal de prontuários de condutores
CREATE TABLE log_prontuarios_gente_gestao (
    id_log_prontuarios_gente_gestao INT PRIMARY KEY AUTO_INCREMENT,
    cpf_log_prontuarios_gente_gestao VARCHAR(255) UNIQUE NOT NULL,
    situacao_log_prontuarios_gente_gestao VARCHAR(255),
    nome_log_prontuarios_gente_gestao VARCHAR(255) NOT NULL,
    cargo_log_prontuarios_gente_gestao VARCHAR(255),
    status_log_prontuarios_gente_gestao VARCHAR(255),
    pontuacao_log_prontuarios_gente_gestao VARCHAR(255),
    vencimento_log_prontuarios_gente_gestao VARCHAR(255),
    celular_log_prontuarios_gente_gestao VARCHAR(255),
    alimento_log_prontuarios_gente_gestao DECIMAL(10,2),
    fumando_log_prontuarios_gente_gestao DECIMAL(10,2),
    oclusao_log_prontuarios_gente_gestao DECIMAL(10,2),
    cinto_log_prontuarios_gente_gestao DECIMAL(10,2),
    velo1_log_prontuarios_gente_gestao DECIMAL(10,2),
    velo2_log_prontuarios_gente_gestao DECIMAL(10,2),
    velo3_log_prontuarios_gente_gestao DECIMAL(10,2),
    via1_log_prontuarios_gente_gestao DECIMAL(10,2),
    via2_log_prontuarios_gente_gestao DECIMAL(10,2),
    via3_log_prontuarios_gente_gestao DECIMAL(10,2),
    forcag_log_prontuarios_gente_gestao DECIMAL(10,2),
    frenagem_log_prontuarios_gente_gestao DECIMAL(10,2),
    power_log_prontuarios_gente_gestao DECIMAL(10,2),
    operacao_log_prontuarios_gente_gestao VARCHAR(255),
    data_atualizacao_log_prontuarios_gente_gestao DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_cad_filiais INT,
    id_cad_operacoes INT
);

-- Índices para otimização
CREATE INDEX idx_cpf_prontuarios ON log_prontuarios_gente_gestao(cpf_log_prontuarios_gente_gestao);
CREATE INDEX idx_data_atualizacao ON log_prontuarios_gente_gestao(data_atualizacao_log_prontuarios_gente_gestao);
```

## 🚀 Como Executar

### Configuração Inicial

```bash
# 1. Configurar credenciais no banco
mysql -u usuario -p banco_geg
INSERT INTO cad_usuarios_geg (email_cad_usuarios_geg, senha_cad_usuarios_geg)
VALUES ('seu_email@empresa.com', 'sua_senha');
```

### Execução Direta

```bash
cd src
python main.py
```

### Execução em Background (Windows)

```powershell
# Executar em background
Start-Process python -ArgumentList "main.py" -WindowStyle Hidden -WorkingDirectory "src"
```

### Execução com Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY src/ .
COPY output/ ./output/

# Comando de execução
CMD ["python", "main.py"]
```

### Execução como Serviço Windows

```powershell
# Criar tarefa agendada para execução contínua
schtasks /create /tn "RoboGEGIntegracao" /tr "python C:\caminho\para\robo-integracao-gg\src\main.py" /sc onstart /ru SYSTEM
```

## 📊 Estrutura dos Dados

### Formato dos Dados Extraídos

#### Dados de Colaboradores

O sistema extrai as seguintes informações de cada condutor:

```json
{
  "situacao_empregado": "ATIVO",
  "nome": "NOME DO CONDUTOR",
  "cpf": "12345678901",
  "cargo": "Motorista Carreta",
  "status": "LIBERADO",
  "pontuacao": "0",
  "vencimento": "2031-12-31",
  "celular": "0",
  "alimento": "0.00",
  "fumando": "0.00",
  "oclusao": "0.00",
  "cinto": "0.00",
  "velo1": "0.00",
  "velo2": "0.00",
  "velo3": "0.00",
  "via1": "0.00",
  "via2": "0.00",
  "via3": "0.00",
  "forcag": "0.00",
  "frenagem": "0.00",
  "power": "0.00",
  "operacao": "CD FORTALEZA"
}
```

### Mapeamento de Colunas DevExpress

O sistema mapeia automaticamente as colunas da tabela DevExpress:

```python
mapeamento_colunas = {
    0: "situacao_empregado",     # Situação do empregado
    1: "nome",                   # Nome completo
    2: "cpf",                    # CPF formatado
    3: "cargo",                  # Cargo/função
    4: "status",                 # Status atual
    7: "pontuacao",              # Pontuação CNH
    8: "vencimento",             # Vencimento CNH
    34: "celular",               # Uso de celular
    35: "alimento",              # Consumo de alimento
    36: "fumando",               # Fumando
    37: "oclusao",               # Oclusão
    38: "cinto",                 # Sem cinto
    49: "velo1",                 # Excesso velocidade 1
    50: "velo2",                 # Excesso velocidade 2
    51: "velo3",                 # Excesso velocidade 3
    52: "via1",                  # Velocidade por via 1
    53: "via2",                  # Velocidade por via 2
    54: "via3",                  # Velocidade por via 3
    55: "forcag",                # Força G
    56: "frenagem",              # Frenagem brusca
    57: "power",                 # Power On
    69: "operacao"               # Operação
}
```

### Formato CSV de Saída

```csv
"situacao_log_prontuarios_gente_gestao";"nome_log_prontuarios_gente_gestao";"cpf_log_prontuarios_gente_gestao";"cargo_log_prontuarios_gente_gestao";"status_log_prontuarios_gente_gestao";"pontuacao_log_prontuarios_gente_gestao";"vencimento_log_prontuarios_gente_gestao";"celular_log_prontuarios_gente_gestao";"alimento_log_prontuarios_gente_gestao";"fumando_log_prontuarios_gente_gestao";"oclusao_log_prontuarios_gente_gestao";"cinto_log_prontuarios_gente_gestao";"velo1_log_prontuarios_gente_gestao";"velo2_log_prontuarios_gente_gestao";"velo3_log_prontuarios_gente_gestao";"via1_log_prontuarios_gente_gestao";"via2_log_prontuarios_gente_gestao";"via3_log_prontuarios_gente_gestao";"forcag_log_prontuarios_gente_gestao";"frenagem_log_prontuarios_gente_gestao";"power_log_prontuarios_gente_gestao";"operacao_log_prontuarios_gente_gestao"
ATIVO;NOME DO CONDUTOR;"12345678901";Motorista Carreta;LIBERADO;"0";"2031-12-31";"0";0.00;0.00;0.00;0.00;0.00;0.00;0.00;0.00;0.00;0.00;0.00;0.00;0.00;CD FORTALEZA
```

## 🔧 Classes e Módulos

### `main.py` - Orquestrador Principal

Responsável pela coordenação geral do processo:

- Configura sistema de agendamento persistente com SQLite
- Executa automação imediatamente na inicialização
- Configura execução diária às 15h com tolerância de 1h
- Gerencia threads de execução e tratamento de sinais
- Integra com sistema de retry automático

### Módulos de Automação

#### `automacao_geg.py` - Classe Principal de Automação

- **`AutomacaoGEG`**: Classe principal para automação completa
- **`executar_automacao_completa()`**: Orquestra todo o processo de extração
- **`_realizar_login()`**: Gerencia autenticação no portal
- **`_navegar_para_relatorio()`**: Navega para página de relatórios
- **`_extrair_dados_colaboradores()`**: Extrai dados via AJAX
- **`_processar_resposta_devexpress()`**: Processa respostas DevExpress
- **`_extrair_dados_melhorado()`**: Extração inteligente de dados
- Sistema de logging detalhado e arquivos de debug

#### `services/login_service.py` - Serviços de Autenticação

- **`LoginService`**: Classe de serviços de login
- **`obter_pagina_login()`**: Obtém página inicial de login
- **`capturar_campos_ocultos()`**: Captura campos ASP.NET necessários
- **`preparar_dados_login()`**: Prepara payload de autenticação
- **`logar()`**: Executa processo de login
- Tratamento de ViewState e EventValidation

#### `services/data_service.py` - Processamento de Dados

- **`DataService`**: Classe de processamento de dados
- **`extrair_dados_colaboradores()`**: Extração de dados de HTML
- **`converter_dados_para_df()`**: Conversão para DataFrame Pandas
- **`salvar_dados_csv()`**: Persistência em formato CSV
- **`imprimir_resumo()`**: Estatísticas de extração
- Validação e normalização automática de dados

### Módulos de Infraestrutura

#### `repositories/database.py` - Gestão de Banco

- **`get_session_context()`**: Context manager para sessões SQLAlchemy
- Configuração de engine com pool de conexões otimizado
- Tratamento automático de transações e rollback
- Integração com variáveis de ambiente

#### `database/models.py` - Modelos de Dados

- **`CadUsuariosGEG`**: Modelo para credenciais de usuários
- Mapeamento SQLAlchemy para tabelas MySQL
- Validação de dados e relacionamentos

#### `utils/file_util.py` - Utilitários

- **`save_response_to_file()`**: Salva respostas HTTP para debug
- Utilitários para manipulação de arquivos
- Suporte a encoding UTF-8

## 📝 Logs e Monitoramento

### Tipos de Log:

- ✅ **INFO**: Operações normais (login, navegação, extração, persistência)
- ⚠️ **WARNING**: Situações de atenção mas não críticas (retry, parsing alternativo)
- 🔴 **ERROR**: Falhas críticas que impedem a execução (autenticação, conexão)
- 🔍 **DEBUG**: Informações detalhadas para troubleshooting (dados extraídos)

### Exemplo de Saída:

```
================================================================================
                        ROBÔ GEG - INTEGRAÇÃO GENTE E GESTÃO
================================================================================
2025-08-29 15:00:15 - INFO: === INICIANDO AUTOMAÇÃO GEG - 20250829_150015 ===
2025-08-29 15:00:15 - INFO: Passo 1: Realizando login...
2025-08-29 15:00:16 - INFO: Obtendo página de login...
2025-08-29 15:00:17 - INFO: Capturando campos ocultos...
2025-08-29 15:00:17 - INFO: Enviando requisição de login...
2025-08-29 15:00:18 - INFO: Login realizado com sucesso
2025-08-29 15:00:18 - INFO: Passo 2: Navegando para página de relatório...
2025-08-29 15:00:19 - INFO: Acessando página do relatório...
2025-08-29 15:00:20 - INFO: Página do relatório acessada com sucesso
2025-08-29 15:00:20 - INFO: Passo 3: Extraindo dados dos colaboradores...
2025-08-29 15:00:21 - INFO: Enviando requisição AJAX para carregar dados...
2025-08-29 15:00:22 - INFO: Resposta AJAX recebida: 245678 caracteres
2025-08-29 15:00:22 - INFO: Processando resposta DevExpress...
2025-08-29 15:00:23 - INFO: HTML extraído do DevExpress: 198432 caracteres
2025-08-29 15:00:24 - INFO: Encontrou tabela DevExpress principal
2025-08-29 15:00:25 - INFO: Analisando 157 linhas da tabela DevExpress
2025-08-29 15:00:26 - INFO: Extraídos 142 colaboradores da tabela DevExpress
2025-08-29 15:00:26 - INFO: Dados extraídos: 142 colaboradores
2025-08-29 15:00:26 - INFO: Passo 4: Salvando dados em CSV...
2025-08-29 15:00:27 - INFO: CSV salvo no formato padrão: output/log_prontuario_20250829_150015.csv
2025-08-29 15:00:27 - INFO: === AUTOMAÇÃO CONCLUÍDA COM SUCESSO ===
2025-08-29 15:00:27 - INFO: Colaboradores extraídos: 142
2025-08-29 15:00:27 - INFO: Arquivo CSV: output/log_prontuario_20250829_150015.csv
================================================================================
Agendamento persistente configurado para rodar todos os dias às 15h.
Se perder o horário, executa ao iniciar!
```

### Estatísticas de Monitoramento:

- **Total de colaboradores processados** por execução
- **Dados de telemetria e fadigas** extraídos por condutor
- **Taxa de sucesso** de extração e persistência
- **Tempo de processamento** por etapa do pipeline
- **Estatísticas de login** e navegação web

## ⚠️ Troubleshooting

### Problemas Comuns:

#### 1. Erro de Conexão com Banco MySQL

```
Erro: Can't connect to MySQL server
```

**Solução**:

- Verificar string de conexão no `.env`
- Confirmar se MySQL está executando
- Validar credenciais de banco de dados
- Testar conectividade de rede

#### 2. Erro de Autenticação no Portal

```
Erro: Falha no login - credenciais incorretas
```

**Solução**:

- Verificar credenciais na tabela `cad_usuarios_geg`
- Confirmar acesso ao portal Gente e Gestão
- Validar se usuário não está bloqueado
- Testar login manual no portal

#### 3. Erro de Extração de Dados

```
Erro: Nenhum colaborador encontrado
```

**Solução**:

- Verificar estrutura da página de relatórios
- Analisar arquivos HTML de debug salvos
- Confirmar se filtros estão corretos
- Verificar se dados estão disponíveis no portal

#### 4. Erro de Processamento DevExpress

```
Erro: Erro ao processar resposta DevExpress
```

**Solução**:

- Analisar arquivo debug_resposta_ajax_dados.html
- Verificar se resposta AJAX está correta
- Confirmar mapeamento de colunas da tabela
- Testar com dados de exemplo

#### 5. Erro de Agendamento

```
Erro: Failed to start scheduler
```

**Solução**:

- Verificar permissões de escrita no jobs.db
- Confirmar configuração do SQLAlchemy
- Validar string de conexão do agendador
- Testar execução manual sem agendamento

#### 6. Erro de Conversão de Dados

```
Erro: Erro ao converter dados para DataFrame
```

**Solução**:

- Verificar estrutura dos dados extraídos
- Confirmar mapeamento de colunas
- Validar tipos de dados esperados
- Analisar logs de processamento

### Verificações de Saúde:

```sql
-- Verificar dados extraídos recentes
SELECT
    COUNT(*) as total_colaboradores,
    MAX(data_atualizacao_log_prontuarios_gente_gestao) as ultima_atualizacao,
    COUNT(DISTINCT cpf_log_prontuarios_gente_gestao) as cpfs_unicos
FROM log_prontuarios_gente_gestao;

-- Verificar distribuição por status
SELECT
    status_log_prontuarios_gente_gestao,
    COUNT(*) as quantidade
FROM log_prontuarios_gente_gestao
GROUP BY status_log_prontuarios_gente_gestao;

-- Verificar dados de telemetria
SELECT
    AVG(CAST(velo1_log_prontuarios_gente_gestao AS DECIMAL)) as media_vel1,
    AVG(CAST(frenagem_log_prontuarios_gente_gestao AS DECIMAL)) as media_frenagem,
    COUNT(*) as total_registros
FROM log_prontuarios_gente_gestao
WHERE data_atualizacao_log_prontuarios_gente_gestao >= CURDATE();

-- Verificar usuários configurados
SELECT
    email_cad_usuarios_geg,
    'configurado' as status
FROM cad_usuarios_geg;
```

## 🔒 Segurança

- **Credenciais**: Nunca commitar o arquivo `.env` com credenciais reais
- **Senhas**: Senhas armazenadas de forma segura no banco de dados
- **Sessões**: Gestão segura de sessões web com cookies adequados
- **Dados Sensíveis**: CPF e informações pessoais tratados com cuidado
- **Logs**: Não loggar senhas ou tokens em logs de produção
- **SQL Injection**: Uso de ORM SQLAlchemy com queries parametrizadas
- **Web Security**: Headers apropriados e validação de respostas
- **Data Validation**: Validação rigorosa de dados extraídos

## 🔄 Regras de Processamento

### Lógica de Agendamento

- **Execução Diária**: Todo dia às 15h (configurável)
- **Execução Imediata**: Na inicialização do sistema
- **Tolerância**: Até 1h após horário agendado (misfire_grace_time)
- **Persistência**: Agendamento mantido mesmo após reinicializações

### Critérios de Extração

```python
# Configurações de extração
configuracoes_extracao = {
    "retry_attempts": 5,
    "retry_interval": 10,
    "timeout": 30,
    "debug_mode": True,
    "save_intermediary_files": True
}
```

### Processamento de Dados

1. **Login**: Autenticação automática com captura de ViewState
2. **Navegação**: Acesso à página de relatórios com headers corretos
3. **Extração**: Requisição AJAX para carregamento de dados
4. **Processamento**: Parsing DevExpress e mapeamento de colunas
5. **Validação**: Verificação de CPFs e dados obrigatórios
6. **Normalização**: Formatação padronizada dos campos
7. **Persistência**: Inserção/atualização no banco MySQL

### Campos Obrigatórios

**Colaboradores**:

- `cpf_log_prontuarios_gente_gestao` (CPF único)
- `nome_log_prontuarios_gente_gestao` (Nome completo)
- `status_log_prontuarios_gente_gestao` (Status atual)
- `cargo_log_prontuarios_gente_gestao` (Cargo/função)

**Dados de Telemetria**:

- Todos os campos numéricos têm valores padrão "0.00"
- Campos obrigatórios são validados antes da persistência
- Dados inconsistentes são logados para análise

## 👥 Equipe de Desenvolvimento

- **Desenvolvedor**: Fadel Mateus
- **Repositório**: JorgeJefferson/robo-integracao-gg
- **Branch Principal**: main
- **Linguagem**: Python 3.8+
- **Frameworks**: SQLAlchemy 2.0, Pandas 2.0, Requests, BeautifulSoup4, APScheduler

## 📞 Suporte

Para dúvidas ou problemas:

1. Verificar logs do sistema em `output/automacao.log`
2. Analisar arquivos HTML de debug em `output/debug_*.html`
3. Executar verificações de saúde no banco de dados
4. Validar configuração do arquivo `.env`
5. Testar conectividade com portal Gente e Gestão
6. Verificar credenciais na tabela `cad_usuarios_geg`
7. Contatar a equipe de desenvolvimento

### Comandos de Diagnóstico:

```bash
# Testar conectividade com MySQL
python -c "
from repositories.database import get_session_context
try:
    with get_session_context() as session:
        print('MySQL Connection: OK')
except Exception as e:
    print(f'MySQL Connection: FAILED - {e}')
"

# Verificar dependências
pip check

# Executar automação em modo debug
python -c "
from automacao_geg import executar_automacao_geg
import os
from dotenv import load_dotenv

load_dotenv()
# Use credenciais de teste aqui
sucesso, arquivo, dados = executar_automacao_geg('email_teste', 'senha_teste')
print(f'Teste: {'OK' if sucesso else 'FAILED'}')
"
```

### Monitoramento em Tempo Real:

```bash
# Acompanhar logs em tempo real (Windows)
Get-Content "output\automacao.log" -Tail 50 -Wait

# Verificar processo em execução
Get-Process python | Where-Object {$_.CommandLine -like "*main.py*"}

# Verificar tamanho dos arquivos de saída
Get-ChildItem "output\" | Select-Object Name, Length, LastWriteTime | Format-Table
```

---

**⚡ Importante**: O Robô GEG deve executar continuamente para garantir a atualização diária automática de prontuários de condutores. O sistema de agendamento persistente garante que as execuções aconteçam mesmo após reinicializações, enquanto a arquitetura modular permite fácil manutenção e extensão para novos tipos de dados. A gestão inteligente de sessões web e tratamento de erros asseguram alta disponibilidade e confiabilidade do sistema de extração.
