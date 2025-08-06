from json import load
import signal
import threading
from automacao_geg import AutomacaoGEG, executar_automacao_geg
from database.models import CadUsuariosGEG
from services.data_service import DataService
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from repositories.database import get_session_context
from automacao_geg import executar_automacao_geg  # Importa a função de automação
from pymnz.database import update_table_from_dataframe
from dotenv import load_dotenv
import os

load_dotenv(".env")

# Variável de controle para parar o agendador
stop_scheduler = threading.Event()

def signal_handler(signum, frame):
    print("Sinal de interrupção recebido. Encerrando o agendador...")
    stop_scheduler.set()

# Configura o manipulador de sinal para SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def executar_automacao():
    print("Iniciando automação GEG...")
    with get_session_context() as session:
        cad_usuarios_geg = session.query(CadUsuariosGEG)
    if not cad_usuarios_geg:
        print("Nenhuma credencial encontrada no banco de dados.")
        return
    for cred in cad_usuarios_geg:
        print(f"Usando credencial: {cred.email_cad_usuarios_geg}")
        email = str(cred.email_cad_usuarios_geg)
        senha = str(cred.senha_cad_usuarios_geg)
        sucesso, arquivo_csv, colaboradores = executar_automacao_geg(email, senha)
        df = DataService.converter_dados_para_df(colaboradores)
        with get_session_context() as session:
            try:
                update_table_from_dataframe(
                    df=df,
                    table_name="log_prontuarios_gente_gestao",
                    primary_keys=["cpf_log_prontuarios_gente_gestao"],
                    conn=session,
                )
                session.commit()
            except Exception as e:
                print(
                    f"Erro ao atualizar tabela log_prontuarios_gente_gestao: {str(e)}"
                )
            finally:
                session.close()
        if sucesso:
            print(f"Automação concluída com sucesso!")
            print(f"Arquivo CSV: {arquivo_csv}")
            if colaboradores:
                print(f"Colaboradores extraídos: {len(colaboradores)}")
                automacao = AutomacaoGEG()
                stats = automacao.obter_estatisticas(colaboradores)
                print(f"Estatísticas: {stats}")
            else:
                print("Nenhum colaborador foi extraído")
        else:
            print("Erro na automação")

if __name__ == "__main__":
    jobstores = {"default": SQLAlchemyJobStore(url=os.getenv("DATABASE_URL", ""))}
    scheduler = BlockingScheduler(jobstores=jobstores, daemon=True)
    scheduler.add_job(
        executar_automacao,
        "cron",
        hour=15,
        minute=0,
        id="automacao_geg_diaria",
        replace_existing=True,
        misfire_grace_time=3600,  # Executa até 1h depois se perder o horário
    )
    print(
        "Agendamento persistente configurado para rodar todos os dias às 15h.\n"
        "Se perder o horário, executa ao iniciar!"
    )

    # Executa o agendador em um thread separado
    scheduler_thread = threading.Thread(target=scheduler.start)
    scheduler_thread.start()

    # Aguarda até que o sinal de interrupção seja recebido
    try:
        while not stop_scheduler.is_set():  # type: ignore
            stop_scheduler.wait(1)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        print("Interrompendo o agendador...")
        scheduler.shutdown()
        scheduler_thread.join()
        print("Agendador encerrado com sucesso.")
