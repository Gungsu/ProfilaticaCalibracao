import os
import subprocess
import time
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyEventHandler(FileSystemEventHandler):
    contOnModi = 0
    def on_modified(self, event):
        if self.contOnModi == 1:
            self.contOnModi = 0
            return
        if event.is_directory:
            return
        if event.src_path.endswith("softwareInterface.py"):  # Ou o nome do seu script                   
            print("Reiniciando o programa...")
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    vlrInfo = proc.name()
                    name = vlrInfo.lower()  # Correção aqui!
                    cmdline = ' '.join(proc.cmdline()) if proc.cmdline() else ""
                    if "python.exe" in name and "softwareInterface.py" in cmdline:  # Adapte o nome do script
                        print(f"Processo encontrado: PID={proc.pid}")
                        try:
                            proc.kill()
                            print("Processo encerrado com sucesso.")
                        except psutil.NoSuchProcess:
                            print("Processo não encontrado.")
                        except psutil.AccessDenied:
                            print("Sem permissão para encerrar o processo.")
                        except psutil.ZombieProcess:
                            print("Processo zumbi encontrado. Ignorando.")
                        break  # Importante: sair do loop após matar o processo
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    #print("Erro ao acessar informações do processo. Processo pode ter terminado.")
                    continue  # Ignora o processo e continua a busca
            
            subprocess.Popen(["C:/Users/adeus/Documents/PlatformIO/Projects/softwareManutencaoProfilatica/ProfilaticaCalibracao/.venv/Scripts/python.exe", "softwareInterface.py"])  # Ajuste o caminho
            self.contOnModi = 1
                

if __name__ == "__main__":
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    print("Iniciando o programa...")
    subprocess.Popen(["C:/Users/adeus/Documents/PlatformIO/Projects/softwareManutencaoProfilatica/ProfilaticaCalibracao/.venv/Scripts/python.exe", "softwareInterface.py"])  # Ajuste o caminho
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()