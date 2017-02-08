# FoxDot.lib.ServerManager

ServerManager.py

Handles OSC messages being sent to SuperCollider.

## Classes

### `SCLangClient(self, server=None)`

#### Methods

##### `setServer(self, server)`

Associate this Client with given server.
The Client will send from the Server's socket.
The Server will use this Client instance to send replies.

##### `address(self)`

Returns a (host,port) tuple of the remote server this client is
connected to or None if not connected to any server.

##### `__init__(self, server=None)`

Construct an OSC Client.
- server: Local OSCServer-instance this client will use the socket of for transmissions.
If none is supplied, a socket will be created.

##### `connect(self, address)`

Bind to a specific OSC server:
the 'address' argument is a (host, port) tuple
  - host:  hostname of the remote OSC server,
  - port:  UDP-port the remote OSC server listens to.

##### `__eq__(self, other)`

Compare function.
                

##### `_ensureConnected(self, address)`

Make sure client has a socket connected to address

##### `close(self)`

Disconnect & close the Client's socket
                

##### `__ne__(self, other)`

Compare function.
                

##### `sendto(self, msg, address, timeout=None)`

Send the given OSCMessage to the specified address.
  - msg:  OSCMessage (or OSCBundle) to be sent
  - address:  (host, port) tuple specifing remote server to send the message to
  - timeout:  A timeout value for attempting to send. If timeout == None,
        this call blocks until socket is available for writing. 
Raises OSCClientError when timing out while waiting for the socket. 

##### `__str__(self)`

Returns a string containing this Client's Class-name, software-version
and the remote-address it is connected to (if any)

##### `_setSocket(self, skt)`

Set and configure client socket

---

### `SCLangServerManager(self, addr, osc_port, sclang_port)`

#### Methods

##### `start(self)`

Boots SuperCollider 

##### `sendOSC(self, packet)`

Compiles and sends an OSC message for SuperCollider 

##### `makeStartupFile(self)`

Boot SuperCollider and connect over OSC 

---

## Functions

## Data

### `Server`



