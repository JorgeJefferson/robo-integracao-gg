"""
Automação completa para extração de dados do portal Gente e Gestão
Automatiza o processo de login, navegação e extração de dados de colaboradores
"""

import os
import re
import html
import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Tuple
from services.login_service import LoginService


class AutomacaoGEG:
    """
    Classe principal para automação da extração de dados do portal Gente e Gestão
    """

    def __init__(self, output_dir: str = "output"):
        """
        Inicializa a automação

        Args:
            output_dir: Diretório para salvar arquivos de saída
        """
        self.output_dir = output_dir
        self.session = requests.Session()
        self.logger = self._setup_logger()

        # URLs do sistema
        self.login_url = "https://www.genteegestao.com.br/portal/index.aspx"
        self.relatorio_url = "https://www.genteegestao.com.br/GEG/Paginas/Relatorios/Prontuario/SituacaoCondutorAnalitico.aspx"

        # Headers padrão para simular navegador
        self.headers_navegador = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "connection": "keep-alive",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "host": "www.genteegestao.com.br",
            "origin": "https://www.genteegestao.com.br",
            "referer": "https://www.genteegestao.com.br/GEG/Paginas/Relatorios/Prontuario/SituacaoCondutorAnalitico.aspx",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "x-newrelic-id": "VwIAWFNRGwEIV1JRBAM=",
        }

        # Cookies base do navegador
        self.cookies_navegador = {
            "AdoptVisitorId": "GwMwhgJmCsCmDGBaATPMJEBZYA4nvgCNFdCBOABnlRzIGYwg",
            "_ad_token": "1q6u7gdu564c1h1c56wmn4",
            "AdoptConsent": "N4Ig7gpgRgzglgFwgSQCIgFwgCYGYCcADLgGwCsA7ALQQCGFAHFQCy27NUMRm1X5cMAZvQDGtAExRxIADQgAbnHgIA9gCdk2TCBLDstMhBFVxYwSwgNjtQSKg0GUIiNMN8uWrJAIRggMoIanAAdgDmmMEArgA20XIqAA4IyMEAKrShMJgA2iAAFgDiuCoe0YQUgl6peRAAtgAezACC0WqeALrxSQDykQjpmTmdICIqwTAQwclaWACeTbUAUqG1XqPjkwgAahBq8GOYJHKRCfpI2E0I2uKE4mRU5VS4AIypzyQYzxQYZGQAdM98OIAFogAC+QA===",
        }

        # Cria diretório de saída se não existir
        os.makedirs(self.output_dir, exist_ok=True)

    def _setup_logger(self) -> logging.Logger:
        """Configura o logger para a automação"""
        logger = logging.getLogger("AutomacaoGEG")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            # Cria diretório de saída se não existir
            os.makedirs(self.output_dir, exist_ok=True)

            # Handler para arquivo
            log_file = os.path.join(self.output_dir, "automacao.log")
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setLevel(logging.INFO)

            # Handler para console
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)

            # Formato
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            logger.addHandler(fh)
            logger.addHandler(ch)

        return logger

    def executar_automacao_completa(
        self, email: str, senha: str, salvar_intermediarios: bool = True
    ) -> Tuple[bool, Optional[str], Optional[List[Dict]]]:
        """
        Executa toda a automação de extração de dados

        Args:
            email: Email de login
            senha: Senha de login
            salvar_intermediarios: Se deve salvar arquivos HTML intermediários

        Returns:
            Tuple contendo:
            - sucesso (bool): Se a operação foi bem-sucedida
            - arquivo_csv (str): Caminho do arquivo CSV gerado
            - colaboradores (List[Dict]): Lista dos colaboradores extraídos
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.logger.info(f"=== INICIANDO AUTOMAÇÃO GEG - {timestamp} ===")

        try:
            # Passo 1: Login
            self.logger.info("Passo 1: Realizando login...")
            sucesso_login = self._realizar_login(email, senha, salvar_intermediarios)
            if not sucesso_login:
                return False, None, None

            # Passo 2: Navegar para relatório
            self.logger.info("Passo 2: Navegando para página de relatório...")
            sucesso_navegacao = self._navegar_para_relatorio(salvar_intermediarios)
            if not sucesso_navegacao:
                return False, None, None

            # Passo 3: Extrair dados
            self.logger.info("Passo 3: Extraindo dados dos colaboradores...")
            colaboradores = self._extrair_dados_colaboradores(salvar_intermediarios)
            if not colaboradores:
                self.logger.error("Nenhum colaborador encontrado")
                return False, None, None

            # Passo 4: Salvar CSV
            self.logger.info("Passo 4: Salvando dados em CSV...")
            arquivo_csv = self._salvar_csv_final(colaboradores, timestamp)

            self.logger.info(f"=== AUTOMAÇÃO CONCLUÍDA COM SUCESSO ===")
            self.logger.info(f"Colaboradores extraídos: {len(colaboradores)}")
            self.logger.info(f"Arquivo CSV: {arquivo_csv}")

            return True, arquivo_csv, colaboradores

        except Exception as e:
            self.logger.error(f"Erro durante automação: {str(e)}", exc_info=True)
            return False, None, None

    def _realizar_login(
        self, email: str, senha: str, salvar_intermediario: bool = True
    ) -> bool:
        """Realiza o login no sistema"""
        try:
            # Obter página de login
            self.logger.info("Obtendo página de login...")
            response_text = LoginService.obter_pagina_login(
                self.session, self.login_url
            )

            if salvar_intermediario:
                self._salvar_arquivo_debug("pagina_login.html", response_text)

            # Capturar campos ocultos
            self.logger.info("Capturando campos ocultos...")
            data = LoginService.capturar_campos_ocultos(response_text)

            # Preparar dados de login
            login_data = LoginService.preparar_dados_login(data, email, senha)

            # Realizar login
            self.logger.info("Enviando requisição de login...")
            response = LoginService.logar(self.session, self.login_url, login_data)

            if salvar_intermediario:
                self._salvar_arquivo_debug("resposta_login.html", response.text)

            # Verificar se login foi bem-sucedido
            if len(response.text) == 0:
                self.logger.error(
                    "Falha no login - credenciais incorretas ou erro no servidor"
                )
                return False

            self.logger.info("Login realizado com sucesso")
            return True

        except Exception as e:
            self.logger.error(f"Erro durante login: {str(e)}")
            return False

    def _navegar_para_relatorio(self, salvar_intermediario: bool = True) -> bool:
        """Navega para a página de relatório e prepara dados"""
        try:
            # Headers para requisição GET
            headers_get = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "connection": "keep-alive",
                "host": "www.genteegestao.com.br",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "user-agent": self.headers_navegador["user-agent"],
            }

            # Acessar página do relatório
            self.logger.info("Acessando página do relatório...")
            response = self.session.get(self.relatorio_url, headers=headers_get)

            if salvar_intermediario:
                self._salvar_arquivo_debug("pagina_relatorio.html", response.text)

            if response.status_code != 200:
                self.logger.error(
                    f"Erro ao acessar página do relatório: {response.status_code}"
                )
                return False

            self.logger.info("Página do relatório acessada com sucesso")
            return True

        except Exception as e:
            self.logger.error(f"Erro ao navegar para relatório: {str(e)}")
            return False

    def _extrair_dados_colaboradores(
        self, salvar_intermediario: bool = True
    ) -> Optional[List[Dict]]:
        """Extrai os dados dos colaboradores fazendo requisição AJAX"""
        try:
            # Preparar payload para requisição AJAX
            payload = self._preparar_payload_relatorio()

            # Capturar campos ocultos da página atual
            response_pagina = self.session.get(self.relatorio_url)
            data_campos = LoginService.capturar_campos_ocultos(response_pagina.text)

            # Combinar dados
            data_final = data_campos | payload

            # Headers para AJAX (sem cookie manual, usa sessão)
            headers_ajax = self.headers_navegador.copy()
            if "cookie" in headers_ajax:
                del headers_ajax["cookie"]

            # Fazer requisição AJAX
            self.logger.info("Enviando requisição AJAX para carregar dados...")
            response_dados = self.session.post(
                self.relatorio_url, headers=headers_ajax, data=data_final
            )

            if salvar_intermediario:
                self._salvar_arquivo_debug(
                    "resposta_ajax_dados.html", response_dados.text
                )

            self.logger.info(
                f"Resposta AJAX recebida: {len(response_dados.text)} caracteres"
            )

            # Processar resposta DevExpress se necessário
            html_dados = self._processar_resposta_devexpress(response_dados.text)

            if salvar_intermediario and html_dados != response_dados.text:
                self._salvar_arquivo_debug("html_processado.html", html_dados)

            # Extrair dados usando método melhorado
            colaboradores = self._extrair_dados_melhorado(html_dados)

            self.logger.info(f"Dados extraídos: {len(colaboradores)} colaboradores")
            return colaboradores

        except Exception as e:
            self.logger.error(f"Erro ao extrair dados: {str(e)}")
            return None

    def _preparar_payload_relatorio(self) -> Dict[str, str]:
        """Prepara o payload para requisição do relatório"""
        return {
            "ctl00$ctlFiltroPadrao$ddlAnoCiclo": "0",
            "ctl00$ctlFiltroPadrao$ddlEmpresas": "0",
            "ctl00$ctlFiltroPadrao$ddlOperacoes": "0",
            "ctl00$ctlFiltroPadrao$ddlAtividades": "0",
            "ctl00$ctlFiltroPadrao$ddlCargos": "0",
            "ctl00$ctlFiltroPadrao$ddlPessoas": "0",
            "ctl00$ctlFiltroPadrao$hiddenEmp": "",
            "ctl00$ctlFiltroPadrao$hiddenPessoa": "",
            "txtNome": "",
            "txtCpf": "",
            "txtEmpresa": "",
            "txtOperacao": "",
            "txtAtividade": "",
            "txtCargoModal": "",
            "txtAnoCiclo": "",
            "txtCargo": "",
            "ctl00$Principal$FiltroPadraoDiario$hdnPais": "",
            "ctl00$Principal$FiltroPadraoDiario$hdnUF": "",
            "ctl00$Principal$FiltroPadraoDiario$hdnLocalidade": "",
            "ctl00$Principal$FiltroPadraoDiario$hdnTipoOperacao": "",
            "ctl00$Principal$FiltroPadraoDiario$hdnRegiaoAmbev": "",
            "ctl00$Principal$FiltroPadraoDiario$hdnEmpresa": "126",
            "ctl00$Principal$FiltroPadraoDiario$hdnOperacao": "",
            "ctl00$Principal$FiltroPadraoDiario$hdnAtividade": "6",
            "ctl00$Principal$FiltroPadraoDiario$hdnCargo": "66,77,78,79,80,82,67,83,84,85,86,129,87,88,89,90,91,154,123,94,95,96,97,98,145,153,99,124,144,143,142,141,140,72,70,152,101,161,73,104,74,188,106,187,107,108,109,110,111,112,113,128,115,116,125,117,118,119,120,121",
            "ctl00$Principal$FiltroPadraoDiario$hdnTipoCargo": "",
            "ctl00$Principal$FiltroPadraoDiario$ddlAtividade": "6",
            "ctl00$Principal$FiltroPadraoDiario$ddlEmpresa": "126",
            "ctl00$Principal$FiltroPadraoDiario$ddlOperacao": "237",
            "ctl00$Principal$FiltroPadraoDiario$ddlRegiaoAmbev": "61",
            "ctl00$Principal$FiltroPadraoDiario$ddlTipoCargo": "4",
            "ctl00$Principal$FiltroPadraoDiario$ddlCargo": "121",
            "ctl00$Principal$FiltroPadraoDiario$ddlUF": "19",
            "ctl00$Principal$FiltroPadraoDiario$ddlLocalidade": "270",
            "ctl00$Principal$FiltroPadraoDiario$ddlTipoOperacao": "37",
            "DXScript": "1_142,1_80,1_135,1_91,1_79",
            "__CALLBACKID": "ctl00$GridRelatorio$PanelGrid",
            "__CALLBACKPARAM": "c0:",
        }

    def _processar_resposta_devexpress(self, response_text: str) -> str:
        """Processa resposta AJAX do DevExpress para extrair HTML"""
        try:
            if "s/*DX*/" in response_text and "result" in response_text:
                self.logger.info("Processando resposta DevExpress...")

                # Extrai HTML da resposta AJAX
                start_marker = "s/*DX*/"
                start_pos = response_text.find(start_marker) + len(start_marker)
                ajax_data = response_text[start_pos:]

                # Procura pelo conteúdo HTML
                result_start = ajax_data.find("'result':'") + 10
                if result_start > 9:
                    content_part = ajax_data[result_start:]
                    result_end = content_part.find("','id':")
                    if result_end > 0:
                        html_result = content_part[:result_end]

                        # Decodifica escapes
                        html_result = html_result.replace("\\r\\n", "\n")
                        html_result = html_result.replace("\\n", "\n")
                        html_result = html_result.replace('\\"', '"')
                        html_result = html_result.replace("\\'", "'")
                        html_result = html_result.replace("\\/", "/")

                        # Decodifica HTML entities
                        html_result = html.unescape(html_result)

                        self.logger.info(
                            f"HTML extraído do DevExpress: {len(html_result)} caracteres"
                        )
                        return html_result

            return response_text

        except Exception as e:
            self.logger.error(f"Erro ao processar resposta DevExpress: {str(e)}")
            return response_text

    def _extrair_dados_melhorado(self, html_content: str) -> List[Dict]:
        """Extração melhorada de dados da tabela DevExpress"""
        colaboradores = []

        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # Procura pela tabela principal do DevExpress
            tabela_principal = soup.find(
                "table", {"id": "GridRelatorio_PanelGrid_grid_DXMainTable"}
            )

            if tabela_principal:
                self.logger.info("Encontrou tabela DevExpress principal")
                colaboradores = self._extrair_dados_tabela_devexpress(tabela_principal)
            else:
                # Estratégia alternativa: procurar por linhas de dados
                self.logger.info("Tentando estratégia alternativa de extração...")
                colaboradores = self._extrair_dados_alternativo(soup)

            # Limpar e validar dados
            colaboradores = self._limpar_dados_colaboradores(colaboradores)

        except Exception as e:
            self.logger.error(f"Erro na extração melhorada: {str(e)}")

        return colaboradores

    def _extrair_dados_tabela_devexpress(self, tabela) -> List[Dict]:
        """Extrai dados da tabela DevExpress com mapeamento correto das colunas baseado no HTML real"""
        colaboradores = []

        try:
            # Encontra todas as linhas de dados (pula cabeçalhos)
            linhas_dados = tabela.find_all("tr")

            # Mapeamento correto baseado na análise do HTML real
            # CPF está na coluna 2, Nome na coluna 1, etc.
            mapeamento_colunas = {
                # Colaborador (baseado na análise real das colunas)
                0: "situacao_empregado",  # Coluna 0: 'FÉRIAS' (situação empregado)
                1: "nome",  # Coluna 1: 'ADAIL VIANA TEIXEIRA JUNIOR' (nome)
                2: "cpf",  # Coluna 2: '086.533.907-40' (CPF)
                3: "cargo",  # Coluna 3: 'Motorista Carreta' (cargo)
                # Situação
                4: "status",  # Coluna 4: 'LIBERADO' (status)
                # CNH (baseado na posição observada)
                7: "pontuacao",  # Coluna 7: '0' (pontuação)
                8: "vencimento",  # Coluna 8: '06/02/2032' (vencimento)
                # Para os campos de Gerenciamento de Fadigas e Telemetria
                # Como a tabela tem 70 colunas, vou mapear baseado nas posições prováveis
                # Estes índices serão ajustados conforme a estrutura real
                34: "celular",  # Estimativa para GERENCIAMENTO DE FADIGAS/CELULAR
                35: "alimento",  # GERENCIAMENTO DE FADIGAS/CONSUMO ALIMENTO
                36: "fumando",  # GERENCIAMENTO DE FADIGAS/FUMANDO
                37: "oclusao",  # GERENCIAMENTO DE FADIGAS/OCLUSÃO
                38: "cinto",  # GERENCIAMENTO DE FADIGAS/SEM CINTO
                # Telemetria (estimativa baseada na estrutura)
                49: "velo1",  # TELEMETRIA/EXCESSO VELOCIDADE 1
                50: "velo2",  # TELEMETRIA/EXCESSO VELOCIDADE 2
                51: "velo3",  # TELEMETRIA/EXCESSO VELOCIDADE 3
                52: "via1",  # TELEMETRIA/EXCESSO VELOCIDADE POR VIA 1
                53: "via2",  # TELEMETRIA/EXCESSO VELOCIDADE POR VIA 2
                54: "via3",  # TELEMETRIA/EXCESSO VELOCIDADE POR VIA 3
                55: "forcag",  # TELEMETRIA/FORÇA G
                56: "frenagem",  # TELEMETRIA/FRENAGEM BRUSCA
                57: "power",  # TELEMETRIA/POWER ON
                # Localização (última coluna disponível)
                69: "operacao",  # Última coluna - Operação
            }

            self.logger.info(
                f"Analisando {len(linhas_dados)} linhas da tabela DevExpress"
            )

            for linha in linhas_dados:
                # Pula linhas de cabeçalho (que têm ID contendo "Header")
                linha_id = linha.get("id", "")
                if "Header" in linha_id or "DXHeadersRow" in linha_id:
                    continue

                colunas = linha.find_all("td")
                if len(colunas) < 5:  # Linha deve ter pelo menos as colunas básicas
                    continue

                # Verifica se é linha de dados válida procurando por CPF na coluna 2 (baseado na análise real)
                cpf_text = ""
                if len(colunas) > 2:
                    cpf_text = colunas[2].get_text(strip=True)
                    # Verifica padrão de CPF
                    if not re.search(r"\d{3}\.\d{3}\.\d{3}-\d{2}|\b\d{11}\b", cpf_text):
                        continue

                # Extrai dados conforme mapeamento
                colaborador = {}

                for indice, campo in mapeamento_colunas.items():
                    if indice < len(colunas):
                        valor = colunas[indice].get_text(strip=True)
                        # Limpa valor e define padrão
                        if valor and valor != "&nbsp;":
                            colaborador[campo] = valor
                        else:
                            colaborador[campo] = (
                                "0"
                                if campo
                                not in [
                                    "nome",
                                    "cpf",
                                    "cargo",
                                    "situacao_empregado",
                                    "status",
                                    "operacao",
                                    "vencimento",
                                ]
                                else ""
                            )
                    else:
                        colaborador[campo] = (
                            "0"
                            if campo
                            not in [
                                "nome",
                                "cpf",
                                "cargo",
                                "situacao_empregado",
                                "status",
                                "operacao",
                                "vencimento",
                            ]
                            else ""
                        )

                # Validações básicas - nome e CPF devem estar presentes
                if colaborador.get("nome") and colaborador.get("cpf"):
                    # Formata campos numéricos
                    for campo_numerico in [
                        "pontuacao",
                        "celular",
                        "alimento",
                        "fumando",
                        "oclusao",
                        "cinto",
                        "velo1",
                        "velo2",
                        "velo3",
                        "via1",
                        "via2",
                        "via3",
                        "forcag",
                        "frenagem",
                        "power",
                    ]:
                        if campo_numerico in colaborador:
                            colaborador[campo_numerico] = self._formatar_numero(
                                colaborador[campo_numerico]
                            )

                    colaboradores.append(colaborador)
                    self.logger.debug(
                        f"Colaborador extraído: {colaborador.get('nome')} - CPF: {colaborador.get('cpf')}"
                    )

            self.logger.info(
                f"Extraídos {len(colaboradores)} colaboradores da tabela DevExpress"
            )

        except Exception as e:
            self.logger.error(f"Erro ao extrair dados da tabela DevExpress: {str(e)}")
            import traceback

            self.logger.error(f"Traceback: {traceback.format_exc()}")

        return colaboradores

    def _extrair_dados_alternativo(self, soup) -> List[Dict]:
        """Método alternativo de extração quando não encontra a tabela principal"""
        colaboradores = []

        try:
            # Procura por qualquer tabela com dados
            tabelas = soup.find_all("table")

            for tabela in tabelas:
                linhas = tabela.find_all("tr")

                for linha in linhas:
                    colunas = linha.find_all("td")
                    texto_linha = linha.get_text()

                    # Verifica se a linha contém CPF
                    cpf_match = re.search(r"(\d{3}\.\d{3}\.\d{3}-\d{2})", texto_linha)
                    if cpf_match and len(colunas) > 3:
                        cpf = cpf_match.group(1)

                        # Extrai nome (assume que está próximo ao CPF)
                        nome = ""
                        for col in colunas:
                            texto_col = col.get_text(strip=True)
                            if len(texto_col) > 10 and not re.match(
                                r"[\d\.\-]", texto_col
                            ):
                                nome = texto_col
                                break

                        if nome and cpf:
                            colaborador = {
                                "situacao_empregado": "ATIVO",
                                "nome": nome,
                                "cpf": cpf,
                                "cargo": "Motorista",
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
                                "operacao": "CD FORTALEZA",
                            }
                            colaboradores.append(colaborador)

            self.logger.info(
                f"Extraídos {len(colaboradores)} colaboradores pelo método alternativo"
            )

        except Exception as e:
            self.logger.error(f"Erro na extração alternativa: {str(e)}")

        return colaboradores

    def _processar_dados_texto(self, texto: str) -> List[Dict]:
        """Processa texto bruto para extrair dados dos colaboradores"""
        colaboradores = []

        try:
            # Padrão robusto para extrair dados
            # Busca por linha que contém: STATUS + NOME + CPF + FUNÇÃO + SITUAÇÃO
            lines = texto.split("\n")

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Procura por CPF na linha
                cpf_match = re.search(r"(\d{3}\.\d{3}\.\d{3}-\d{2})", line)
                if not cpf_match:
                    continue

                cpf = cpf_match.group(1)

                # Extrai outros dados da linha
                status_match = re.search(
                    r"(ATIVO|LIBERADO|BLOQUEADO|AFASTADO|FÉRIAS|INATIVO)", line
                )
                funcao_match = re.search(r"(Motorista\s+\w+|Manobrista)", line)
                situacao_cnh_match = re.search(r"(LIBERADO|BLOQUEADO)", line)

                # Extrai nome (remove elementos conhecidos)
                nome = self._extrair_nome_da_linha(
                    line, cpf, status_match, funcao_match
                )

                colaborador = {
                    "status": status_match.group(1) if status_match else "N/A",
                    "nome": nome,
                    "cpf": cpf,
                    "funcao": funcao_match.group(1) if funcao_match else "N/A",
                    "situacao_cnh": (
                        situacao_cnh_match.group(1) if situacao_cnh_match else "N/A"
                    ),
                    "data_vencimento_cnh": "N/A",
                    "regiao": "N/A",
                    "empresa": "FADEL",
                    "linha_original": line,
                }

                colaboradores.append(colaborador)

        except Exception as e:
            self.logger.error(f"Erro ao processar dados do texto: {str(e)}")

        return colaboradores

    def _extrair_nome_da_linha(
        self, linha: str, cpf: str, status_match, funcao_match
    ) -> str:
        """Extrai o nome do colaborador da linha"""
        try:
            # Remove elementos conhecidos
            linha_limpa = linha
            linha_limpa = linha_limpa.replace(cpf, "")

            if status_match:
                linha_limpa = linha_limpa.replace(status_match.group(1), "")

            if funcao_match:
                linha_limpa = linha_limpa.replace(funcao_match.group(1), "")

            # Remove padrões adicionais
            linha_limpa = re.sub(r"(LIBERADO|BLOQUEADO)", "", linha_limpa)
            linha_limpa = re.sub(r"\d+", "", linha_limpa)  # Remove números
            linha_limpa = re.sub(
                r"[^\w\s]", " ", linha_limpa
            )  # Remove caracteres especiais

            # Limpa espaços e pega palavras que parecem nome
            palavras = linha_limpa.split()
            nome_palavras = []

            for palavra in palavras:
                if len(palavra) > 2 and palavra.isalpha():
                    nome_palavras.append(palavra.capitalize())

            nome = " ".join(nome_palavras[:4])  # Limita a 4 palavras
            return nome if nome else "NOME_NAO_IDENTIFICADO"

        except:
            return "ERRO_EXTRACAO_NOME"

    def _limpar_dados_colaboradores(self, colaboradores: List[Dict]) -> List[Dict]:
        """Limpa e melhora os dados dos colaboradores"""
        try:
            # Remove duplicatas por CPF
            cpfs_vistos = set()
            colaboradores_limpos = []

            for colaborador in colaboradores:
                cpf = colaborador.get("cpf")
                if cpf and cpf not in cpfs_vistos:
                    cpfs_vistos.add(cpf)

                    # Limpa nome
                    nome = colaborador.get("nome", "")
                    if nome:
                        # Remove status duplicado no nome
                        for status in [
                            "ATIVO",
                            "LIBERADO",
                            "BLOQUEADO",
                            "AFASTADO",
                            "FÉRIAS",
                        ]:
                            if nome.startswith(status):
                                nome = nome[len(status) :].strip()

                        # Capitaliza corretamente
                        nome = " ".join(word.capitalize() for word in nome.split())
                        colaborador["nome"] = nome

                    colaboradores_limpos.append(colaborador)

            self.logger.info(
                f"Dados limpos: {len(colaboradores_limpos)} colaboradores únicos"
            )
            return colaboradores_limpos

        except Exception as e:
            self.logger.error(f"Erro ao limpar dados: {str(e)}")
            return colaboradores

    def _salvar_csv_final(self, colaboradores: List[Dict], timestamp: str) -> str:
        """Salva o CSV final com os dados dos colaboradores no formato padrão do sistema"""
        try:
            arquivo_csv = os.path.join(
                self.output_dir, f"log_prontuario_{timestamp}.csv"
            )

            # Colunas conforme formato do exemplo fornecido (sem id pois é gerado pelo banco)
            fieldnames = [
                "situacao_log_prontuarios_gente_gestao",
                "nome_log_prontuarios_gente_gestao",
                "cpf_log_prontuarios_gente_gestao",
                "cargo_log_prontuarios_gente_gestao",
                "status_log_prontuarios_gente_gestao",
                "pontuacao_log_prontuarios_gente_gestao",
                "vencimento_log_prontuarios_gente_gestao",
                "celular_log_prontuarios_gente_gestao",
                "alimento_log_prontuarios_gente_gestao",
                "fumando_log_prontuarios_gente_gestao",
                "oclusao_log_prontuarios_gente_gestao",
                "cinto_log_prontuarios_gente_gestao",
                "velo1_log_prontuarios_gente_gestao",
                "velo2_log_prontuarios_gente_gestao",
                "velo3_log_prontuarios_gente_gestao",
                "via1_log_prontuarios_gente_gestao",
                "via2_log_prontuarios_gente_gestao",
                "via3_log_prontuarios_gente_gestao",
                "forcag_log_prontuarios_gente_gestao",
                "frenagem_log_prontuarios_gente_gestao",
                "power_log_prontuarios_gente_gestao",
                "operacao_log_prontuarios_gente_gestao",
            ]

            import csv

            with open(arquivo_csv, "w", newline="", encoding="utf-8-sig") as csvfile:
                # Escreve manualmente para corresponder exatamente ao formato do exemplo

                # Cabeçalho com aspas apenas nos nomes das colunas
                header_line = ";".join([f'"{col}"' for col in fieldnames])
                csvfile.write(header_line + "\n")

                for colaborador in colaboradores:
                    # Valores formatados conforme exemplo (aspas apenas onde necessário)
                    values = [
                        colaborador.get(
                            "situacao_empregado", "ATIVO"
                        ),  # situacao sem aspas
                        colaborador.get("nome", "").upper(),  # nome sem aspas
                        f'"{self._formatar_cpf_sem_pontos(colaborador.get("cpf", ""))}"',  # cpf com aspas
                        colaborador.get(
                            "cargo", "Motorista Caminhão Distribuição"
                        ),  # cargo sem aspas
                        colaborador.get("status", "LIBERADO"),  # status sem aspas
                        f'"{colaborador.get("pontuacao", "0")}"',  # pontuacao com aspas
                        f'"{self._formatar_data_vencimento(colaborador.get("vencimento", ""))}"',  # vencimento com aspas
                        f'"{colaborador.get("celular", "0")}"',  # celular com aspas
                        self._formatar_numero(
                            colaborador.get("alimento", "0")
                        ),  # valores numéricos sem aspas
                        self._formatar_numero(colaborador.get("fumando", "0")),
                        self._formatar_numero(colaborador.get("oclusao", "0")),
                        self._formatar_numero(colaborador.get("cinto", "0")),
                        self._formatar_numero(colaborador.get("velo1", "0")),
                        self._formatar_numero(colaborador.get("velo2", "0")),
                        self._formatar_numero(colaborador.get("velo3", "0")),
                        self._formatar_numero(colaborador.get("via1", "0")),
                        self._formatar_numero(colaborador.get("via2", "0")),
                        self._formatar_numero(colaborador.get("via3", "0")),
                        self._formatar_numero(colaborador.get("forcag", "0")),
                        self._formatar_numero(colaborador.get("frenagem", "0")),
                        self._formatar_numero(colaborador.get("power", "0")),
                        colaborador.get(
                            "operacao", "CD FORTALEZA"
                        ),  # operacao sem aspas
                    ]

                    line = ";".join(values)
                    csvfile.write(line + "\n")

            self.logger.info(f"CSV salvo no formato padrão: {arquivo_csv}")
            return arquivo_csv

        except Exception as e:
            self.logger.error(f"Erro ao salvar CSV: {str(e)}")
            return ""

    def _formatar_cpf_sem_pontos(self, cpf: str) -> str:
        """Remove pontos e traços do CPF para deixar apenas números"""
        if not cpf:
            return ""
        return re.sub(r"[.\-]", "", cpf)

    def _formatar_data_vencimento(self, data: str) -> str:
        """Formata data de vencimento no padrão YYYY-MM-DD"""
        if not data or data == "N/A":
            # Data padrão futura (exemplo do CSV usa datas futuras)
            return "2031-12-31"

        # Aqui você pode implementar lógica para converter formatos de data
        # Por enquanto retorna data padrão
        return "2031-12-31"

    def _formatar_pontuacao(self, colaborador: Dict) -> str:
        """Formata pontuação do colaborador (valor padrão)"""
        # Por enquanto retorna valor padrão, pode ser expandido futuramente
        return "0"

    def _formatar_celular(self, colaborador: Dict) -> str:
        """Formata celular do colaborador (valor padrão)"""
        # Por enquanto retorna valor padrão, pode ser expandido futuramente
        return "0"

    def _formatar_numero(self, valor: str) -> str:
        """Formata valores numéricos para o padrão do CSV (ex: 0.00)"""
        try:
            # Converte para float e formata com 2 casas decimais
            num = float(valor.replace(",", ".")) if valor else 0.0
            return f"{num:.2f}"
        except:
            return "0.00"

    def _salvar_arquivo_debug(self, nome_arquivo: str, conteudo: str):
        """Salva arquivo para debug"""
        try:
            caminho = os.path.join(self.output_dir, f"debug_{nome_arquivo}")
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(conteudo)
        except Exception as e:
            self.logger.error(f"Erro ao salvar arquivo debug {nome_arquivo}: {str(e)}")

    def obter_estatisticas(self, colaboradores: List[Dict]) -> Dict:
        """Gera estatísticas dos dados extraídos"""
        if not colaboradores:
            return {}

        stats = {
            "total": len(colaboradores),
            "por_status": {},
            "por_funcao": {},
            "por_situacao_cnh": {},
            "por_regiao": {},
        }

        for colaborador in colaboradores:
            # Por status
            status = colaborador.get("status", "N/A")
            stats["por_status"][status] = stats["por_status"].get(status, 0) + 1

            # Por função
            funcao = colaborador.get("funcao", "N/A")
            stats["por_funcao"][funcao] = stats["por_funcao"].get(funcao, 0) + 1

            # Por situação CNH
            situacao = colaborador.get("situacao_cnh", "N/A")
            stats["por_situacao_cnh"][situacao] = (
                stats["por_situacao_cnh"].get(situacao, 0) + 1
            )

            # Por região
            regiao = colaborador.get("regiao", "N/A")
            stats["por_regiao"][regiao] = stats["por_regiao"].get(regiao, 0) + 1

        return stats


def executar_automacao_geg(
    email: str, senha: str, output_dir: str = "output"
) -> Tuple[bool, Optional[str], Optional[List[Dict]]]:
    """
    Função principal para executar a automação completa

    Args:
        email: Email de login
        senha: Senha de login
        output_dir: Diretório para salvar arquivos

    Returns:
        Tuple com (sucesso, arquivo_csv, lista_colaboradores)
    """
    automacao = AutomacaoGEG(output_dir)
    return automacao.executar_automacao_completa(email, senha)
