import threading
import socket

host = '127.0.0.1' #Host local
porta = 40000 #Nao reservada

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Cria conexao TCP
server.bind((host, porta)) #associa IP e porta
server.listen() #Inicia a espera

clients = [] #Lista de clientes
nomes = [] #Nomes dos usuários

def transmitir(mensagem): #Mandar para todos os clientes a mensagem no chat
    for client in clients:
        client.send(mensagem)

def receber(client): #Receber as mensagens dos clientes
    while True:
        try: #Enviar pra todos a mensagem recebida
            mensagem = client.recv(1024)
            transmitir(mensagem)
            print(mensagem.decode('ascii'))
        except: #Desconectar um client em caso de erro ou saída
            i = clients.index(client) #Pega a posiçao do cliente
            clients.remove(client)  #Tira ele da lista
            client.close() #Encerra a conexão com ele
            nome = nomes[i] #Acha o nome dele
            transmitir('{} saiu do chat.'.format(nome).encode('ascii'))
            nomes.remove(nome) # Tira o nome dele

def conectar():
    while True:
        client, IP = server.accept()
        print(f'{IP} está conectado')

        client.send('NOME'.encode('ascii'))
        nome = client.recv(1024).decode('ascii')
        nomes.append(nome)
        clients.append(client)

        print(f'O nome do novo usuario é: {nome}')

        transmitir(f'{nome} entrou no chat' .encode('ascii'))
        client.send("Conectado!".encode('ascii'))

        thread = threading.Thread(target=receber, args=(client,))
        thread.start()

print('Servidor conectado! Esperando clientes...')
conectar()
        