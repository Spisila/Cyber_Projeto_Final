import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clientes = []

#Função de broadcast
def broadcast(mensagem, cliente_atual):
  for cliente in clientes:
    if cliente != cliente_atual: 
      try:
          cliente.sendall(mensagem)
      except:
          pass

def lidar_com_cliente(conexao, endereco):
  
  print(f"Cliente conectado: {endereco}")
  clientes.append(conexao)

  try:

    #Loop de receber mensagens
    while True:
      mensagem = conexao.recv(1024)

      texto = mensagem.decode().strip()
      print(f"[{endereco}] {texto}")

      broadcast(mensagem, conexao)

  except:
    print(f"Problema com o cliente {endereco}")

  finally :
    print(f"Cliente {endereco} desconectado")
    clientes.remove(conexao)
    conexao.close()

def iniciar_servidor():

  #Cria o socket, bind no endereço e escuta 
  servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  servidor.bind((HOST, PORT))
  servidor.listen()

  print(f"Ouvindo em {HOST}:{PORT}")

  #Loop do servidor
  while True:
    #Conexao do cliente no server threads
    conexao, endereco = servidor.accept()
    thread = threading.Thread(target=lidar_com_cliente, args=(conexao, endereco))
    thread.start()

if __name__ == "__main__":
  iniciar_servidor()