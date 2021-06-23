import socket  

s = socket.socket()         
host = socket.gethostname() 
port = 3000             
s.bind((host, port))       

s.listen(5)           
conn, addr = s.accept()

with conn:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        else:
            print(data.decode('utf-8'))
