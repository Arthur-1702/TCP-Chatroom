import threading
import socket
import tkinter as tk

nome = input('Digite seu nome: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Cria conexao TCP
client.connect(('127.0.0.1', 40000)) #conecta no IP e porta

def entraServidor():
    while True:
        try:
            mensagem = client.recv(1024).decode('ascii')
            if mensagem == 'NOME':
                client.send(nome.encode('ascii'))
            else:
                print(mensagem)
        except:
            print('Erro!')
            client.close()
            break

def escreveMensagem():
    while True:
        mensagem = '{}: {}'.format(nome, input(''))
        client.send(mensagem.encode('ascii'))


threadReceber = threading.Thread(target=entraServidor)
threadReceber.start()

threadEscrever = threading.Thread(target=escreveMensagem)
threadEscrever.start()

