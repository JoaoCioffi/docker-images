import subprocess
import time
import requests

def docker_compose_up():
    print("\n🐳 Iniciando Metabase via Docker Compose...\n")
    try:
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
        print("\n🟢 Container iniciado.")
        print("🔗 Metabase UI: http://localhost:3000\n")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Falha ao iniciar container: {e}")
        return False
    return True

def wait_for_metabase(max_attempts=60):
    print("\n⏳ Aguardando Metabase ficar pronto...\n")
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:3000/api/health", timeout=5)
            if response.status_code == 200:
                print("\n✅ Metabase está pronto!\n")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(2)
        print(f"   Tentativa {attempt + 1}/{max_attempts}...")
    
    print("[ERROR] Metabase não ficou pronto a tempo.")
    return False

def docker_compose_down():
    print("\n🧹 Encerrando container...\n")
    try:
        subprocess.run(["docker", "compose", "down"], check=True)
        print("\n[INFO] Container finalizado com sucesso.\n")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Erro ao parar container: {e}")

if __name__ == "__main__":
    if docker_compose_up():
        if wait_for_metabase():
            try:
                print("\n⏳ Pressione CTRL+C para parar o container.\n")
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                docker_compose_down()
        else:
            print("\n[ERROR] Encerrando devido a falha na inicialização do Metabase.")
            docker_compose_down()
