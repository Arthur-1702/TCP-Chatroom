import socket
import threading

PORT = 50000 #porta livre
SERVER = '127.0.0.1' #IP Local
ADDRESS = (SERVER, PORT)

FORMAT = "utf-8" #Formatação padrão

clients = [] #Listas para salvar os clientes e seus nomes
users = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #criando socket TCP

server.bind(ADDRESS) #colocando endereço IP/Porta no servidor


def criaConexão(): #Iniciar e esperar conecção com clientes

	print("Servidor esperando clientes...")
	server.listen()
	
	while True:
	
		
		clienteConectado, ipCliente = server.accept()
		clienteConectado.send("NAME".encode(FORMAT)) #aceita o cliente e manda uma requisição (pede o nome)
		
		user = clienteConectado.recv(1024).decode(FORMAT) #recebe a resposta da requisição (nome do usuário)

		users.append(user)
		clients.append(clienteConectado) #adiciona o nome e client da nova conexão nas listas
		
		print(f"Novo usuário :{user}") 
		

		transmitir(f"{user} entrou no chat!".encode(FORMAT)) #Anuncia aos usuários a entrada do novo
		
		clienteConectado.send('Conexão feita!'.encode(FORMAT)) #Envia ao conectado uma mensagem de conexão
		
		#Cria uma thread para cada cliente
		thread = threading.Thread(target = trataMensagens, args = (clienteConectado, ipCliente))
		thread.start()
		
		print(f"Conexões ativas: {threading.activeCount()-1}") #Avisa quantos clientes(threads) simultaneos


def trataMensagens(clienteConectado, ipCliente): #recebe as mensagens e retransmite

	print(f"Nova conexão: {ipCliente}")

	while True:
		
		mensagem = clienteConectado.recv(1024) #recebe
		transmitir(mensagem) #retransmite
	
	clienteConectado.close() #fecha a conexão com cliente sempre que terminar

def transmitir(mensagem): #transmite mensagens para todos os clientes
	for client in clients:
		client.send(mensagem)

criaConexão() 
