import socket
import threading
import time
import sys

HOST = '127.0.0.1'
PORT = 5001
nickname = "Anonimo"

def receber_mensagens(client_socket):
  while True:
    try:
      data, _ = client_socket.recvfrom(1024)
      print(data.decode('utf-8'))
    except:
      break

def benchmark(client_socket, size_bytes):
    print(f"Iniciando Benchmark UDP ({size_bytes} bytes)")
    #Cria o payload, um buffer com varios caracteres 'x'
    data = b'x' * size_bytes
    start_time = time.time()
    try:
      client_socket.sendto(data, (HOST, PORT))
      end_time = time.time()
      print(f"Tempo de despacho UDP: {end_time - start_time:.5f} segundos")
    except Exception as e:
      print(f"Erro no benchmark: {e}")

def main():
  global nickname
  cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  
  #Pacote inicial vazio para o servidor registrar o IP e Porta
  cliente.sendto(f"Entrou: {nickname}".encode('utf-8'), (HOST, PORT))

  #Cria o thread do cliente
  thread = threading.Thread(target=receber_mensagens, args=(cliente,))
  thread.start()

  print("UDP Conectado! Comandos: /nick, /bench, /sair")

  while True:
    mensagem = input()
    if mensagem.startswith('/sair'):
      cliente.close()
      sys.exit()
    elif mensagem.startswith('/nick'):
      partes_mensagem = mensagem.split(' ')
      if len(partes_mensagem) > 1: nickname = partes_mensagem[1]
    elif mensagem.startswith('/bench'):
      partes_mensagem = mensagem.split(' ')
      if len(partes_mensagem) > 1: benchmark(cliente, int(partes_mensagem[1]))
    else:
      mensagem_completa = f"{nickname}: {mensagem}"
      cliente.sendto(mensagem_completa.encode('utf-8'), (HOST, PORT))

if __name__ == "__main__":
  main()