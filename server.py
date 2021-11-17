import socket
import threading

# Porta livre e IP local 
PORT = 50000
SERVER = '127.0.0.1'
ADDRESS = (SERVER, PORT)

# formato padrão pra encode e decode
FORMAT = "utf-8"

# criando socket tcp do server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# associa o socket com endereço ip/porta
server.bind(ADDRESS)

# listas de clientes e nomes de usuário
clients, users = [], []

# espera os clientes se conectarem
def esperaConexao():

	print("Servidor iniciado e esperando conexões...")
	server.listen()
	
	while True:
	
		# aceita as conexões e recebe o endereço
		cliente, ip = server.accept()
		cliente.send("NAME".encode(FORMAT))
		
		# recebe o nome do cliente com limite maximo de bytes
		user = cliente.recv(1024).decode(FORMAT)
		
		# coloca o cliente e seu respectivo user nas listas
		users.append(user)
		clients.append(cliente)
		
		print(f"Nome :{user}")
		
		# avisa ao conectado que está no chat
		cliente.send('Conectado ao chat! '.encode(FORMAT))

		# avisa aos clientes que alguém entrou
		transmite(f" {user} acaba de entrar!".encode(FORMAT))
				
		# começa a thread
		thread = threading.Thread(target = mensagens, args = (cliente, ip))
		thread.start()
		
		# numero de clientes (sockets) conectados
		print(f"active connections {threading.activeCount()-1}")

# lida com as mensagens recebidas
def mensagens(cliente, ip):

	print(f"Nova conexão: {ip}")
	conectado = True
	
	while conectado:
		# recebe a mensagem do cliente
		msg = cliente.recv(1024)
		
		# retransmite a mensagem
		transmite(msg)
	
	# fecha a conexao após
	cliente.close()

# transmite a mensagem para todos os clientes
def transmite(msg):
	for client in clients:
		client.send(msg)


esperaConexao()
