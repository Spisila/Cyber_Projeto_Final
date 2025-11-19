import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clientes = []

def enviar_para_todos(msg, cliente_atual):
    for c in clientes:
        if c != cliente_atual: 
            try:
                c.sendall(msg)
            except:
                pass

def lidar_com_cliente(conn, addr):
    print(f"[CONEXÃO] Cliente conectado: {addr}")
    clientes.append(conn)

    try:
        while True:
            msg = conn.recv(1024)
            if not msg:
                break

            texto = msg.decode().strip()
            print(f"[{addr}] {texto}")

            enviar_para_todos(msg, conn)

    except:
        print(f"[ERRO] Problema com o cliente {addr}")

    print(f"[DESCONECTADO] {addr}")
    clientes.remove(conn)
    conn.close()

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()

    print(f"[SERVIDOR] Ouvindo em {HOST}:{PORT}")

    while True:
        conn, addr = servidor.accept()
        thread = threading.Thread(target=lidar_com_cliente, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    iniciar_servidor()