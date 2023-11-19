import socket,pickle,time

HOST=#Server IP
port=6543
FORMAT='UTF-8'

def eq(a:str, b:str, c:str) ->bool:
	if a==b:
		if b==c:
			return True
	return False

class board:

	def __init__(self,b):
		self.b=b
	def __repr__(self):
		toR =""
		for i in range(9):
			j=i+1
			if j%3==0:
				toR=toR+"|"+self.b[i]+"| \n"+"-"*7+"\n"
			else:
				toR+="|"+self.b[i]
		return toR
	
	def checkwin(self) ->list[bool,str]:
		for i in range(0,9,3):
			if eq(self.b[i],self.b[i+1],self.b[i+2]) and self.b[i]!="_":
				if self.b[i]!="_":
					return [True, self.b[i]]			
		
		for i in range(3):
			if eq(self.b[i],self.b[i+3],self.b[i+6]) and self.b[i]!="_":
				return [True, self.b[i]]
			
		if eq(self.b[0],self.b[4],self.b[8]) and self.b[0]!="_":
			return [True, self.b[0]]
		
		if eq(self.b[2],self.b[4],self.b[6]) and self.b[2]!="_":
			return [True, self.b[4]]
		
		return [False]
		
	def sqLeft(self):
		for sq in self.b:
			if sq=="_":
				return True
	
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST,port))
	data=s.recv(1024)
	print(data.decode('UTF-8'))
	data=s.recv(1024)
	if data.decode(FORMAT)=="T":
		print("PLAYER 1")
		while True:
			time.sleep(1)
			game = pickle.loads(s.recv(4096))
			print(game)
			if game.checkwin()[0]:
				print(f"{game.checkwin()[1]} has won")
				break
			if not game.sqLeft():
				print("DRAW")
				break
			invalid=True
			while invalid:
				move = input("Enter your move") 
				if move.isdigit():
					move=int(move)
					if move<10 and move>0:
						move = move-1
						if game.b[move]=="_":
							move=str(move)
							s.send(move.encode(FORMAT))
							game.b[int(move)]="X"
							invalid = False
			if game.checkwin()[0]:
				print(f"{game.checkwin()[1]} has won")
				break
			if not game.sqLeft():
				print("DRAW")
				break

	else:
		print("PLAYER 2")
		while True:
			print("Waiting for Player 1 to move")
			time.sleep(1)
			game = pickle.loads(s.recv(4096))
			print(game)
			if game.checkwin()[0]:
				print(f"{game.checkwin()[1]} has won")
				break
			elif not game.sqLeft():
				print("DRAW")
			invalid=True
			while invalid:
				move = input("Enter your move") 
				if move.isdigit():
					move=int(move)
					if move<10 and move>0:
						move = move-1
						if game.b[move]=="_":
							move=str(move)
							s.send(move.encode(FORMAT))
							game.b[int(move)]="O"
							invalid=False

			if game.checkwin()[0]:
				print(f"{game.checkwin()[1]} has won")
				break
			if not game.sqLeft():
				print("DRAW")
				break
	#data=s.recv(1024)
	#data=pickle.loads(data)
	#print(data.decode(FORMAT))
	#s.send(input(">>> ").encode('UTF-8'))

