import signal
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from config.settings import settings

# Variável de controle para parar o agendador
stop_scheduler = threading.Event()

def signal_handler(signum, frame):
    print("Sinal de interrupção recebido. Encerrando o agendador...")
    stop_scheduler.set()

# Configura o manipulador de sinal para SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def executar_automacao():
    print("🚀 Iniciando automação GEG...")
    # (O código da função `executar_automacao` permanece o mesmo)

if __name__ == "__main__":
    database_url = settings.database_url or "sqlite:///default.db"
    jobstores = {"default": SQLAlchemyJobStore(url=database_url)}
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
        while not stop_scheduler.is_set():
            stop_scheduler.wait(1)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        print("Interrompendo o agendador...")
        scheduler.shutdown()
        scheduler_thread.join()
        print("Agendador encerrado com sucesso.")
