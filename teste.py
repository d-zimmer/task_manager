import subprocess

def abrir_agendador_tarefas():
    try:
        subprocess.run(['calc'])
    except Exception as e:
        print(f"Erro ao abrir a Calculadora: {e}")

if __name__ == '__main__':
    abrir_agendador_tarefas()
