import socket

HOST = '0.0.0.0'
PORT = 5001 

#Usando um set ao invez de um array para conexao UDP
clientes = set()

def start_server():

  #Criação do socket e bind no endereço
  server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  server.bind((HOST, PORT))

  print(f"[INICIANDO] Servidor UDP rodando em {HOST}:{PORT}")

  #Loop do server
  while True:
    try:
      #Receber dados da socket
      data, endereço = server.recvfrom(1024)
      
      #Se o endereço não esta no set de clientes ele é adicionado
      if endereço not in clientes:
        clientes.add(endereço)
        print(f"Novo cliente : {endereço}")

      #Decodificar mensagem e mostrar ela no console
      mensagem_decodificada = data.decode('utf-8')
      print(f"[{endereço}] {mensagem_decodificada}")

      #Broadcast da mensagem
      for client_endereço in clientes:
        if client_endereço != endereço:
          try:
            server.sendto(data, client_endereço)
          except:
            #Se acontecer erro no envio remover cliente
            clientes.remove(client_endereço)
                  
    except Exception as erro:
      print(f"[ERRO] {erro}")

if __name__ == "__main__":
    start_server()