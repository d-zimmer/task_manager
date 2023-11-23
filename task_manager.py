import os
import win32com.client
from datetime import datetime, timedelta, timezone
from log_manager import LogManager

def get_action_info(actions):
    # Retorna informações sobre a ação da tarefa, incluindo Path e Arguments
    for action in actions:
        try:
            if hasattr(action, 'Path') and hasattr(action, 'Arguments'):
                return {'Path': action.Path, 'Arguments': action.Arguments}
        except Exception as action_error:
            print(f"Erro ao obter informações da ação: {action_error}")

    return {'Path': '', 'Arguments': ''}

def agendar_tarefa(local_script, lista_scripts, log_manager):
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')

    for nome_script in lista_scripts:
        try:
            script_path = os.path.abspath(os.path.join(local_script, nome_script))
            
            # Verifica se o script realmente existe
            if not os.path.isfile(script_path):
                log_manager.handle_task_scheduling_error(f'Script {nome_script} não encontrado', nome_script)
                continue
            
            task_def = scheduler.NewTask(0)

            # Create trigger
            start_time = datetime.now() + timedelta(minutes=1)  # Ajuste os minutos conforme necessário
            TASK_TRIGGER_TIME = 1
            trigger = task_def.Triggers.Create(TASK_TRIGGER_TIME)
            trigger.StartBoundary = start_time.isoformat()

            # Create action
            TASK_ACTION_EXEC = 0
            action = task_def.Actions.Create(TASK_ACTION_EXEC)
            action.ID = 'DO NOTHING'
            action.Path = 'C:/Users/david/AppData/Local/Programs/Python/Python311/python.exe'
            action.Arguments = f'"{script_path}"'

            # Set parameters
            task_def.RegistrationInfo.Description = f'Tarefa Agendada pelo Script Python - {nome_script}'
            task_def.Settings.Enabled = True
            task_def.Settings.StopIfGoingOnBatteries = False

            # Register task
            TASK_CREATE_OR_UPDATE = 6
            TASK_LOGON_NONE = 0
            root_folder.RegisterTaskDefinition(
                nome_script.replace('.', '_'),
                task_def,
                TASK_CREATE_OR_UPDATE,
                '',
                '',
                TASK_LOGON_NONE
            )

            log_manager.append_information_to_file(f'Tarefa agendada: {nome_script} em {start_time}', nome_script)

        except Exception as e:
            log_manager.handle_task_scheduling_error(f'Erro ao agendar tarefa: {str(e)}', nome_script)

    log_manager.print_summary()

if __name__ == '__main__':
    caminho_script = r"C:/Users/david/Documents/task_manager"  # Certifique-se de ajustar o caminho com a unidade do disco correto
    nomes_scripts = input('Digite os nomes dos seus scripts separados por espaço: ').split()

    log_manager = LogManager()
    agendar_tarefa(caminho_script, nomes_scripts, log_manager)
