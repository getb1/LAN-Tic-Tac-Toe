import socket
import threading
import pickle,time
ADDRESS='' # IP ADDRESS OF SERVER
PORT=6543

ACTIVEGAMES=0
MAXCONNECTIONS = 10
numOfCons=0


# Format for sending messages and adress of server
DISCONMESSAGE = "!DISCON"
ADDR=(ADDRESS,PORT)
FORMAT='UTF-8'

#List to store threads of active games
games=[]

# Board class for pickling objects
class board:
	def __init__(self,b):
		self.b=b


def MATCH(clients:list):
	# Handles the individual matches being played at one time
	player1 = clients[0]
	player2 = clients[1]
	print(f"Connected from {player1[1]} amd {player2[1]}")
	game=board(['_' for i in range(9)])
	time.sleep(1)
	player1[0].send("T".encode(FORMAT))
	time.sleep(1)
	player2[0].send("F".encode(FORMAT))
	        
	while True:
		try:
			y=player1[0].send(pickle.dumps(game))


			data = player1[0].recv(1024).decode(FORMAT)

			game.b[int(data)]="X"

			player2[0].send(pickle.dumps(game))
			data=player2[0].recv(1024).decode(FORMAT)
			game.b[int(data)]="O"
			print(game.b,data)
		#end the connection to the server
		except:
			player1[0].close()
			player2[0].close()
			break


def start():
	numOfCons=0
	data=[]
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
		server.bind(ADDR)
		server.listen()
		print(f"[LISTENING] sever is on {ADDR}")
		while threading.active_count()<6:
			conn,addr=server.accept()
			print("NEW CON")
			
			conn.send("WELCOME".encode(FORMAT))
			data.append([conn,addr])
			numOfCons+=1
			if len(data)>=2:
				x=threading.Thread(target=MATCH, args=[[data[0],data[1]]])
				data.pop(0)
				data.pop(0)
				x.start()
				games.append(x)
				print(threading.active_count())
			#conn.close()

		
start()
