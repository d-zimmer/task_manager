from datetime import datetime
import os

class LogManager:
    def __init__(self, log_file_path="logfile.csv"):
        self.log_file_path = log_file_path
        self.successful_tasks = []
        self.failed_tasks = []

    def get_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_script_name(self):
        return os.path.basename(__file__)

    def get_pid(self):
        return os.getpid()

    def append_information_to_file(self, additional_info, script_name=None, success=True):
        with open(self.log_file_path, "a") as log:
            log.write(f"Time: {self.get_time()}, Script Name: {self.get_script_name()}, PID: {self.get_pid()}, {additional_info}\n")

        if success:
            self.successful_tasks.append(script_name)
        else:
            self.failed_tasks.append(script_name)

    def handle_task_scheduling_error(self, error_message, script_name=None):
        self.append_information_to_file(f'Erro ao agendar tarefa ({script_name}): {error_message}', script_name, success=False)

    def print_summary(self):
        print("Scripts Agendados com Sucesso:")
        for script in self.successful_tasks:
            print(f"- {script}")

        print("\nScripts com Erro:")
        for script in self.failed_tasks:
            print(f"- {script}")
