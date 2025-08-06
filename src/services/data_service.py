from bs4 import BeautifulSoup
import pandas as pd
import re
import csv


class DataService:
    @staticmethod
    def extrair_dados_colaboradores(html_content):
        """
        Extrai os dados dos colaboradores da tabela HTML
        """
        soup = BeautifulSoup(html_content, "html.parser")
        colaboradores = []

        # Procura pela tabela principal - pode ser uma div com classe específica ou table
        # Baseado na imagem, parece ser uma grid/tabela com dados dos condutores

        # Tenta encontrar linhas da tabela de diferentes formas
        linhas_tabela = []

        # Método 1: Procura por tabelas tradicionais
        tabelas = soup.find_all("table")
        for tabela in tabelas:
            linhas = tabela.find_all("tr")
            if len(linhas) > 1:  # Tem header + dados
                linhas_tabela.extend(linhas[1:])  # Skip header

        # Método 2: Procura por divs que podem representar linhas de dados
        if not linhas_tabela:
            # Procura por padrões comuns em grids ASP.NET
            grid_rows = soup.find_all("div", class_=re.compile(r".*row.*|.*item.*"))
            linhas_tabela.extend(grid_rows)

        # Método 3: Procura por elementos que contenham dados específicos (CPF, nomes, etc)
        if not linhas_tabela:
            # Procura por elementos que contenham padrões de CPF
            elementos_cpf = soup.find_all(text=re.compile(r"\d{3}\.\d{3}\.\d{3}-\d{2}"))
            for elemento in elementos_cpf:
                # Pega o elemento pai que pode conter toda a linha de dados
                linha_pai = elemento.parent
                while linha_pai and linha_pai.name not in ["tr", "div"]:
                    linha_pai = linha_pai.parent
                if linha_pai:
                    linhas_tabela.append(linha_pai)

        print(f"Encontradas {len(linhas_tabela)} linhas de dados")

        for linha in linhas_tabela:
            colaborador = DataService._extrair_dados_linha(linha)
            if colaborador:
                colaboradores.append(colaborador)

        return colaboradores

    @staticmethod
    def _extrair_dados_linha(linha_elemento):
        """
        Extrai dados específicos de uma linha da tabela
        """
        try:
            # Extrai todo o texto da linha
            texto_linha = linha_elemento.get_text(separator=" ", strip=True)

            # Padrões para extrair informações específicas
            # CPF: ###.###.###-##
            cpf_match = re.search(r"(\d{3}\.\d{3}\.\d{3}-\d{2})", texto_linha)

            # Nome: geralmente aparece antes do CPF ou em posição específica
            # Status: ATIVO, LIBERADO, etc.
            status_match = re.search(
                r"(ATIVO|INATIVO|LIBERADO|BLOQUEADO|AFASTADO|FÉRIAS)", texto_linha
            )

            # Empresa/Categoria: Manobrista, Motorista Carreta, etc.
            categoria_match = re.search(r"(Manobrista|Motorista\s+\w+)", texto_linha)

            if cpf_match:
                colaborador = {
                    "linha_completa": texto_linha,
                    "cpf": cpf_match.group(1) if cpf_match else None,
                    "status": status_match.group(1) if status_match else None,
                    "categoria": categoria_match.group(1) if categoria_match else None,
                }

                # Tenta extrair o nome (geralmente está entre o status e o CPF)
                partes = texto_linha.split()
                colaborador["nome"] = DataService._extrair_nome(partes, colaborador)

                return colaborador

        except Exception as e:
            print(f"Erro ao processar linha: {e}")

        return None

    @staticmethod
    def _extrair_nome(partes_texto, colaborador_data):
        """
        Tenta extrair o nome do colaborador das partes do texto
        """
        try:
            # Remove elementos conhecidos para isolar o nome
            texto_limpo = " ".join(partes_texto)

            # Remove CPF
            if colaborador_data.get("cpf"):
                texto_limpo = texto_limpo.replace(colaborador_data["cpf"], "")

            # Remove status
            if colaborador_data.get("status"):
                texto_limpo = texto_limpo.replace(colaborador_data["status"], "")

            # Remove categoria
            if colaborador_data.get("categoria"):
                texto_limpo = texto_limpo.replace(colaborador_data["categoria"], "")

            # Limpa espaços extras e pega palavras que parecem nomes
            palavras = texto_limpo.split()
            nome_palavras = []

            for palavra in palavras:
                # Considera como parte do nome se tem mais de 2 caracteres e não é número
                if len(palavra) > 2 and not palavra.isdigit() and palavra.isalpha():
                    nome_palavras.append(palavra)

            return " ".join(nome_palavras[:4])  # Limita a 4 palavras para o nome

        except:
            return None

    @staticmethod
    def salvar_dados_csv(colaboradores, arquivo="colaboradores.csv"):
        """
        Salva os dados dos colaboradores em um arquivo CSV
        """
        if colaboradores:
            # Usa o módulo csv padrão do Python
            with open(arquivo, "w", newline="", encoding="utf-8-sig") as csvfile:
                if colaboradores:
                    fieldnames = colaboradores[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(colaboradores)

            print(f"Dados salvos em {arquivo}")
            return True
        return False

    @staticmethod
    def imprimir_resumo(colaboradores):
        """
        Imprime um resumo dos dados extraídos
        """
        print(f"\n=== RESUMO DOS DADOS EXTRAÍDOS ===")
        print(f"Total de colaboradores encontrados: {len(colaboradores)}")

        if colaboradores:
            # Conta por status
            status_count = {}
            for colaborador in colaboradores:
                status = colaborador.get("status", "Não identificado")
                status_count[status] = status_count.get(status, 0) + 1

            print("\nDistribuição por status:")
            for status, count in status_count.items():
                print(f"  {status}: {count}")

            # Mostra alguns exemplos
            print(f"\nPrimeiros 3 registros:")
            for i, colaborador in enumerate(colaboradores[:3]):
                print(f"  {i+1}. Nome: {colaborador.get('nome', 'N/A')}")
                print(f"     CPF: {colaborador.get('cpf', 'N/A')}")
                print(f"     Status: {colaborador.get('status', 'N/A')}")
                print(f"     Categoria: {colaborador.get('categoria', 'N/A')}")
                print()


    @staticmethod
    def converter_dados_para_df(colaboradores):
        """
        Converte a lista de colaboradores para um DataFrame do pandas, padronizando colunas e tipos
        """
        import pandas as pd

        if not colaboradores:
            return None

        # Cria DataFrame
        df = pd.DataFrame(colaboradores)

        # Mapeamento de operações para IDs
        OPERACOES_MAP = {
            "NOVA RIO": {"id_cad_filiais": 2, "id_cad_operacoes": 2},
            "NOVA MINAS": {"id_cad_filiais": 3, "id_cad_operacoes": 2},
        }

        # Conversão de datas e atualização de timestamp
        df["vencimento"] = pd.to_datetime(
            df["vencimento"],
            errors="coerce",
            format="%d/%m/%Y",
        )
        df["data_atualizacao"] = pd.Timestamp.now()

        # Renomeia colunas para padrão do banco
        df.columns = [f"{col}_log_prontuarios_gente_gestao" for col in df.columns]

        # Aplica mapeamento de IDs de operação/filial
        df["id_cad_filiais"] = df["operacao_log_prontuarios_gente_gestao"].map(
            lambda op: OPERACOES_MAP.get(op, {}).get("id_cad_filiais", 0)
        )
        df["id_cad_operacoes"] = df["operacao_log_prontuarios_gente_gestao"].map(
            lambda op: OPERACOES_MAP.get(op, {}).get("id_cad_operacoes", 0)
        )

        return df
