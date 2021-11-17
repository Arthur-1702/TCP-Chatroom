import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk

# Porta livre e IP local 
PORT = 50000
SERVER = '127.0.0.1'
ADDRESS = (SERVER, PORT)
# formato padrão pra encode e decode
FORMAT = "utf-8"

# cria um socket pro cliente e conecta no server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

# classe de GUI do chat
class GUI:
	
	def __init__(self):
	
		# janela do chat escondida
		self.Window = Tk()
		self.Window.withdraw()
		
		# janela de login (user)
		self.login = Toplevel()
		# titulo
		self.login.title("Login")
		# tamanho da tela
		self.login.resizable(width = True, height = True)
		self.login.configure(width = 850, height = 600)

		# cria texto pedindo nome
		self.pls = Label(self.login,
					text = "Digite seu usuário para entrar",
					justify = CENTER,
					font = "Adobe 30 bold")
		self.pls.place(relheight = 0.1,
					relx = 0.15,
					rely = 0.07)
		
		# cria texto antes da caixa de texto
		self.labelName = Label(self.login,
							text = "Usuário: ",
							font = "Tekton 20")
		
		self.labelName.place(relheight = 0.2,
							relx = 0.1,
							rely = 0.25)
		
		# cria a caixa de texto para nome
		self.entryName = Entry(self.login,
							font = "Fixedsys 20")
		
		self.entryName.place(relwidth = 0.4,
							relheight = 0.12,
							relx = 0.30,
							rely = 0.3)
		
		# da o foco do cursos de texto
		self.entryName.focus()
		
		# cria o botão para entrar no chat e da o comando pra enviar o nome
		self.go = Button(self.login,
						text = "ENTRAR",
						font = "Fixedsys 20 bold",
						command = lambda: self.avançar(self.entryName.get()))
		
		self.go.place(relx = 0.4,
					rely = 0.55)
		self.Window.mainloop()

	# vai do login para a segunda tela (chat)
	def avançar(self, name):
		self.login.destroy()
		self.layout(name)
		
		# a thread para receber mensagens
		rcv = threading.Thread(target=self.receive)
		rcv.start()

	# tela do chat
	def layout(self,name):
	
		self.name = name
		# mostra a tela do chat
		self.Window.deiconify()
		self.Window.title("CHAT")
		self.Window.resizable(width = True,
							height = True)
		self.Window.configure(width = 470,
							height = 550,
							bg = "#17202A")
		self.labelHead = Label(self.Window,
							bg = "#17202A",
							fg = "#EAECEE",
							text = self.name ,
							font = "Helvetica 13 bold",
							pady = 5)
		
		self.labelHead.place(relwidth = 1)
		self.line = Label(self.Window,
						width = 450,
						bg = "#ABB2B9")
		
		self.line.place(relwidth = 1,
						rely = 0.07,
						relheight = 0.012)
		
		self.textCons = Text(self.Window,
							width = 20,
							height = 2,
							bg = "#17202A",
							fg = "#EAECEE",
							font = "Helvetica 14",
							padx = 5,
							pady = 5)
		
		self.textCons.place(relheight = 0.745,
							relwidth = 1,
							rely = 0.08)
		
		self.labelBottom = Label(self.Window,
								bg = "#ABB2B9",
								height = 80)
		
		self.labelBottom.place(relwidth = 1,
							rely = 0.825)
		
		self.entryMsg = Entry(self.labelBottom,
							bg = "#2C3E50",
							fg = "#EAECEE",
							font = "Helvetica 13")
		
		# place the given widget
		# into the gui window
		self.entryMsg.place(relwidth = 0.74,
							relheight = 0.06,
							rely = 0.008,
							relx = 0.011)
		
		self.entryMsg.focus()
		
		# create a Send Button
		self.buttonMsg = Button(self.labelBottom,
								text = "Send",
								font = "Helvetica 10 bold",
								width = 20,
								bg = "#ABB2B9",
								command = lambda : self.sendButton(self.entryMsg.get()))
		
		self.buttonMsg.place(relx = 0.77,
							rely = 0.008,
							relheight = 0.06,
							relwidth = 0.22)
		
		self.textCons.config(cursor = "arrow")
		
		# create a scroll bar
		scrollbar = Scrollbar(self.textCons)
		
		# place the scroll bar
		# into the gui window
		scrollbar.place(relheight = 1,
						relx = 0.974)
		
		scrollbar.config(command = self.textCons.yview)
		
		self.textCons.config(state = DISABLED)

	# function to basically start the thread for sending messages
	def sendButton(self, msg):
		self.textCons.config(state = DISABLED)
		self.msg=msg
		self.entryMsg.delete(0, END)
		snd= threading.Thread(target = self.sendMessage)
		snd.start()

	# function to receive messages
	def receive(self):
		while True:
			try:
				message = client.recv(1024).decode(FORMAT)
				
				# if the messages from the server is NAME send the client's name
				if message == 'NAME':
					client.send(self.name.encode(FORMAT))
				else:
					# insert messages to text box
					self.textCons.config(state = NORMAL)
					self.textCons.insert(END,
										message+"\n\n")
					
					self.textCons.config(state = DISABLED)
					self.textCons.see(END)
			except:
				# an error will be printed on the command line or console if there's an error
				print("An error occured!")
				client.close()
				break
		
	# function to send messages
	def sendMessage(self):
		self.textCons.config(state=DISABLED)
		while True:
			message = (f"{self.name}: {self.msg}")
			client.send(message.encode(FORMAT))
			break

# create a GUI class object
g = GUI()
