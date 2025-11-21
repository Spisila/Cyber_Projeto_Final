import socket
import threading
import time
import sys

HOST = '127.0.0.1' 
PORT = 5000

nickname = "Anonimo"

def receber_mensagens(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Erro Conexão perdida.")
            client_socket.close()
            break

def benchmark(client_socket, size_bytes):

    print(f"--- Iniciando Benchmark TCP ({size_bytes} bytes) ---")
    #Cria o payload, um buffer com varios caracteres 'x'
    data = b'x' * size_bytes 
    start_time = time.time()
    try:
        client_socket.send(data)
        end_time = time.time()
        print(f"--- Fim do Benchmark ---")
        print(f"Tempo total de envio: {end_time - start_time:.5f} segundos")
    except Exception as e:
        print(f"Erro no benchmark: {e}")

def main():
    global nickname

    #Cria o socket do cliente
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #Tenta conectar o cliente
    try:
        client.connect((HOST, PORT))
    except:
        print(f"Não foi possível conectar a {HOST}:{PORT}")
        return

    #Começa thread de receber mensagens
    thread = threading.Thread(target=receber_mensagens, args=(client,))
    thread.start()

    print("Conectado! Comandos: /nick <nome>, /bench <bytes>, /sair")

    #Loop de comandos do cliente
    while True:
        mensagem = input()
        
        if mensagem.startswith('/sair'):
            client.close()
            sys.exit()
    
        elif mensagem.startswith('/nick'):
            parts = mensagem.split(' ')
            if len(parts) > 1:
                nickname = parts[1]
                print(f"Apelido alterado para {nickname}")
            else:
                print("Uso: /nick <nome>")
        
        elif mensagem.startswith('/bench'):
            parts = mensagem.split(' ')
            if len(parts) > 1 and parts[1].isdigit():
                benchmark(client, int(parts[1]))
            else:
                print("Uso: /bench <bytes>")
        
        else:
            
            full_msg = f"{nickname}: {mensagem}"
            try:
                client.send(full_msg.encode('utf-8'))
            except:
                break

if __name__ == "__main__":
    main()