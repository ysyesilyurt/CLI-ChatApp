# CLI-ChatApp
A simple Command Line Interface Python Chat Application, simply creates a Chatroom in which a server and several clients can send and receive messages from each other.
 
Created with SocketServer Framework

## Usage
Clone repository
```
git clone https://github.com/ysyesilyurt/CLI-ChatApp
```
Run ```server.py``` with correct parameters, Usage:
```
./server.py [PORT] [HOST]
```
You can also run directly, in that case it defaults to ```10000 localhost```:
```
./server.py 
```
Afterwards clients can connect to the server using ```client.py``` with correct parameters, Usage:
```
./client.py [PORT] [HOST]
```
Default is again, ```10000 localhost```:
```
./client.py 
```

