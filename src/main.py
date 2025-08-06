from automacao_geg import AutomacaoGEG, executar_automacao_geg
from repositories.database import get_session_context
from database.models import CadUsuariosGEG
from pymnz.database import update_table_from_dataframe

from services.data_service import DataService
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from dotenv import load_dotenv
import os


def executar_automacao():
    print("🚀 Iniciando automação GEG...")
    with get_session_context() as session:
        cad_usuarios_geg = session.query(CadUsuariosGEG)
    if not cad_usuarios_geg:
        print("❌ Nenhuma credencial encontrada no banco de dados.")
        return
    for cred in cad_usuarios_geg:
        print(f"🔐 Usando credencial: {cred.email_cad_usuarios_geg}")
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
                    f"⚠️ Erro ao atualizar tabela log_prontuarios_gente_gestao: {str(e)}"
                )
            finally:
                session.close()
        if sucesso:
            print(f"✅ Automação concluída com sucesso!")
            print(f"📄 Arquivo CSV: {arquivo_csv}")
            if colaboradores:
                print(f"👥 Colaboradores extraídos: {len(colaboradores)}")
                automacao = AutomacaoGEG()
                stats = automacao.obter_estatisticas(colaboradores)
                print(f"📊 Estatísticas: {stats}")
            else:
                print("⚠️ Nenhum colaborador foi extraído")
        else:
            print("❌ Erro na automação")


# Carrega variáveis do .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if __name__ == "__main__":
    jobstores = {"default": SQLAlchemyJobStore(url=DATABASE_URL)}
    scheduler = BlockingScheduler(jobstores=jobstores)
    scheduler.add_job(
        executar_automacao,
        "cron",
        hour=16,
        minute=20,
        id="automacao_geg_diaria",
        replace_existing=True,
        misfire_grace_time=3600,  # Executa até 1h depois se perder o horário
    )
    print(
        "⏰ Agendamento persistente configurado para rodar todos os dias às 15h. Se perder o horário, executa ao iniciar!"
    )

    try:
        scheduler.start(True)
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Interrompendo o agendador...")
        scheduler.shutdown()
        print("✅ Agendador encerrado com sucesso.")    
        exit(0)
