# `OSC3`

This module contains an OpenSoundControl implementation (in Pure Python), based
(somewhat) on the good old 'SimpleOSC' implementation by Daniel Holth & Clinton
McChesney.

This implementation is intended to still be 'simple' to the user, but much more
complete (with OSCServer & OSCClient classes) and much more powerful (the
OSCMultiClient supports subscriptions & message-filtering, OSCMessage &
OSCBundle are now proper container-types)

===============================================================================
OpenSoundControl
===============================================================================

OpenSoundControl is a network-protocol for sending (small) packets of addressed
data over network sockets. This OSC-implementation supports the classical 
UDP/IP protocol for sending and receiving packets but provides as well support
for TCP/IP streaming, whereas the message size is prepended as int32 (big
endian) before each message/packet.

OSC-packets come in two kinds:

        - OSC-messages consist of an 'address'-string (not to be confused with a
        (host:port) network-address!), followed by a string of 'typetags'
        associated with the message's arguments (ie. 'payload'), and finally the
        arguments themselves, encoded in an OSC-specific way. The OSCMessage class
        makes it easy to create & manipulate OSC-messages of this kind in a
        'pythonesque' way (that is, OSCMessage-objects behave a lot like lists)

        - OSC-bundles are a special type of OSC-message containing only
        OSC-messages as 'payload'. Recursively. (meaning; an OSC-bundle could
        contain other OSC-bundles, containing OSC-bundles etc.)
        
OSC-bundles start with the special keyword '#bundle' and do not have an
OSC-address (but the OSC-messages a bundle contains will have OSC-addresses!).
Also, an OSC-bundle can have a timetag, essentially telling the receiving
server to 'hold' the bundle until the specified time. The OSCBundle class
allows easy cration & manipulation of OSC-bundles.
        
For further information see also http://opensoundcontrol.org/spec-1_0

-------------------------------------------------------------------------------

To send OSC-messages, you need an OSCClient, and to receive OSC-messages you
need an OSCServer.

The OSCClient uses an 'AF_INET / SOCK_DGRAM' type socket (see the 'socket'
module) to send binary representations of OSC-messages to a remote host:port
address.

The OSCServer listens on an 'AF_INET / SOCK_DGRAM' type socket bound to a local
port, and handles incoming requests. Either one-after-the-other (OSCServer) or
in a multi-threaded / multi-process fashion (ThreadingOSCServer/
ForkingOSCServer). If the Server has a callback-function (a.k.a. handler)
registered to 'deal with' (i.e. handle) the received message's OSC-address,
that function is called, passing it the (decoded) message.

The different OSCServers implemented here all support the (recursive) un-
bundling of OSC-bundles, and OSC-bundle timetags.

In fact, this implementation supports:

        - OSC-messages with 'i' (int32), 'f' (float32), 'd' (double), 's' (string) and
        'b' (blob / binary data) types
        - OSC-bundles, including timetag-support
        - OSC-address patterns including '*', '?', '{,}' and '[]' wildcards.

(please *do* read the OSC-spec! http://opensoundcontrol.org/spec-1_0 it
explains what these things mean.)

In addition, the OSCMultiClient supports:
        - Sending a specific OSC-message to multiple remote servers
        - Remote server subscription / unsubscription (through OSC-messages, of course)
        - Message-address filtering.

-------------------------------------------------------------------------------
SimpleOSC:
        Copyright (c) Daniel Holth & Clinton McChesney.
pyOSC:
        Copyright (c) 2008-2010, Artem Baguinski <artm@v2.nl> et al., Stock, V2_Lab, Rotterdam, Netherlands.
Streaming support (OSC over TCP):
        Copyright (c) 2010 Uli Franke <uli.franke@weiss.ch>, Weiss Engineering, Uster, Switzerland.

-------------------------------------------------------------------------------
Changelog:
-------------------------------------------------------------------------------
v0.3.0  - 27 Dec. 2007
        Started out to extend the 'SimpleOSC' implementation (v0.2.3) by Daniel Holth & Clinton McChesney.
        Rewrote OSCMessage
        Added OSCBundle
        
v0.3.1  - 3 Jan. 2008
        Added OSClient
        Added OSCRequestHandler, loosely based on the original CallbackManager 
        Added OSCServer
        Removed original CallbackManager
        Adapted testing-script (the 'if __name__ == "__main__":' block at the end) to use new Server & Client
        
v0.3.2  - 5 Jan. 2008
        Added 'container-type emulation' methods (getitem(), setitem(), __iter__() & friends) to OSCMessage
        Added ThreadingOSCServer & ForkingOSCServer
                - 6 Jan. 2008
        Added OSCMultiClient
        Added command-line options to testing-script (try 'python OSC.py --help')

v0.3.3  - 9 Jan. 2008
        Added OSC-timetag support to OSCBundle & OSCRequestHandler
        Added ThreadingOSCRequestHandler
        
v0.3.4  - 13 Jan. 2008
        Added message-filtering to OSCMultiClient
        Added subscription-handler to OSCServer
        Added support fon numpy/scipy int & float types. (these get converted to 'standard' 32-bit OSC ints / floats!)
        Cleaned-up and added more Docstrings

v0.3.5 - 14 aug. 2008
        Added OSCServer.reportErr(...) method

v0.3.6 - 19 April 2010
        Added Streaming support (OSC over TCP)
        Updated documentation
        Moved pattern matching stuff into separate class (OSCAddressSpace) to
                facilitate implementation of different server and client architectures.
                Callbacks feature now a context (object oriented) but dynamic function
                inspection keeps the code backward compatible
        Moved testing code into separate testbench (testbench.py)

-----------------
Original Comments
-----------------
> Open SoundControl for Python
> Copyright (C) 2002 Daniel Holth, Clinton McChesney
> 
> This library is free software; you can redistribute it and/or modify it under
> the terms of the GNU Lesser General Public License as published by the Free
> Software Foundation; either version 2.1 of the License, or (at your option) any
> later version.
> 
> This library is distributed in the hope that it will be useful, but WITHOUT ANY
> WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
> PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
> details.
>
> You should have received a copy of the GNU Lesser General Public License along
> with this library; if not, write to the Free Software Foundation, Inc., 59
> Temple Place, Suite 330, Boston, MA  02111-1307  USA
>
> For questions regarding this module contact Daniel Holth <dholth@stetson.edu>
> or visit http://www.stetson.edu/~ProctoLogic/
>
> Changelog:
> 15 Nov. 2001:
>       Removed dependency on Python 2.0 features.
>       - dwh
> 13 Feb. 2002:
>       Added a generic callback handler.
>       - dwh

## Classes

### `ForkingOSCServer(self, server_address, client=None, return_port=0)`

An Asynchronous OSCServer.
This server forks a new process to handle each incoming request.

#### Methods

##### `__eq__(self, other)`

Compare function.
                

##### `__init__(self, server_address, client=None, return_port=0)`

Instantiate an OSCServer.
- server_address ((host, port) tuple): the local host & UDP-port
the server listens on
- client (OSCClient instance): The OSCClient used to send replies from this server.
If none is supplied (default) an OSCClient will be created.
- return_port (int): if supplied, sets the default UDP destination-port
for replies coming from this server.

##### `__ne__(self, other)`

Compare function.
                

##### `__str__(self)`

Returns a string containing this Server's Class-name, software-version and local bound address (if any)
                

##### `_handle_request_noblock(self)`

Handle one request, without blocking.

I assume that selector.select() has returned that the socket is
readable before this function was called, so there should be no risk of
blocking in get_request().

##### `_subscribe(self, data, client_address)`

Handle the actual subscription. the provided 'data' is concatenated together to form a
'<host>:<port>[<prefix>] [<filter>] [...]' string, which is then passed to 
parseUrlStr() & parseFilterStr() to actually retreive <host>, <port>, etc.

This 'long way 'round' approach (almost) guarantees that the subscription works, 
regardless of how the bits of the <url> are encoded in 'data'. 

##### `_unsubscribe(self, data, client_address)`

Handle the actual unsubscription. the provided 'data' is concatenated together to form a
'<host>:<port>[<prefix>]' string, which is then passed to 
parseUrlStr() to actually retreive <host>, <port> & <prefix>.

This 'long way 'round' approach (almost) guarantees that the unsubscription works, 
regardless of how the bits of the <url> are encoded in 'data'. 

##### `addDefaultHandlers(self, prefix=, info_prefix=/info, error_prefix=/error)`

Register a default set of OSC-address handlers with this Server:
- 'default' ->  noCallback_handler
the given prefix is prepended to all other callbacks registered by this method:
- '<prefix><info_prefix' ->  serverInfo_handler
- '<prefix><error_prefix> ->  msgPrinter_handler
- '<prefix>/print' ->  msgPrinter_handler
and, if the used Client supports it;
- '<prefix>/subscribe' -> subscription_handler
- '<prefix>/unsubscribe' -> subscription_handler

Note: the given 'error_prefix' argument is also set as default 'error_prefix' for error-messages
*sent from* this server. This is ok, because error-messages generally do not elicit a reply from the receiver.

To do this with the serverInfo-prefixes would be a bad idea, because if a request received on '/info' (for example)
would send replies to '/info', this could potentially cause a never-ending loop of messages!
Do *not* set the 'info_prefix' here (for incoming serverinfo requests) to the same value as given to
the setSrvInfoPrefix() method (for *replies* to incoming serverinfo requests).
For example, use '/info' for incoming requests, and '/inforeply' or '/serverinfo' or even just '/print' as the 
info-reply prefix. 

##### `addMsgHandler(self, address, callback)`

Register a handler for an OSC-address
  - 'address' is the OSC address-string. 
the address-string should start with '/' and may not contain '*'
  - 'callback' is the function called for incoming OSCMessages that match 'address'.
The callback-function will be called with the same arguments as the 'msgPrinter_handler' below

##### `address(self)`

Returns a (host,port) tuple of the local address this server is bound to,
or None if not bound to any address.

##### `close(self)`

Stops serving requests, closes server (socket), closes used client
                

##### `close_request(self, request)`

Called to clean up an individual request.

##### `delMsgHandler(self, address)`

Remove the registered handler for the given OSC-address
                

##### `dispatchMessage(self, pattern, tags, data, client_address)`

Attmept to match the given OSC-address pattern, which may contain '*',
against all callbacks registered with the OSCServer.
Calls the matching callback and returns whatever it returns.
If no match is found, and a 'default' callback is registered, it calls that one,
or raises NoCallbackError if a 'default' callback is not registered.

  - pattern (string):  The OSC-address of the receied message
  - tags (string):  The OSC-typetags of the receied message's arguments, without ','
  - data (list):  The message arguments

##### `fileno(self)`

Return socket file number.

Interface required by selector.

##### `finish_request(self, request, client_address)`

Finish one request by instantiating RequestHandlerClass.

##### `getOSCAddressSpace(self)`

Returns a list containing all OSC-addresses registerd with this Server. 
                

##### `get_request(self)`

Get the request and client address from the socket.

May be overridden.

##### `handle_error(self, request, client_address)`

Handle an exception in the Server's callbacks gracefully.
Writes the error to sys.stderr and, if the error_prefix (see setSrvErrorPrefix()) is set,
sends the error-message as reply to the client

##### `handle_request(self)`

Handle one request, possibly blocking.

Respects self.timeout.

##### `handle_timeout(self)`

Called if no new request arrives within self.timeout.

Overridden by ForkingMixIn.

##### `msgPrinter_handler(self, addr, tags, data, client_address)`

Example handler for OSCMessages.
All registerd handlers must accept these three arguments:
- addr (string): The OSC-address pattern of the received Message
  (the 'addr' string has already been matched against the handler's registerd OSC-address,
  but may contain '*'s & such)
- tags (string):  The OSC-typetags of the received message's arguments. (without the preceding comma)
- data (list): The OSCMessage's arguments
  Note that len(tags) == len(data)
- client_address ((host, port) tuple): the host & port this message originated from.

a Message-handler function may return None, but it could also return an OSCMessage (or OSCBundle),
which then gets sent back to the client.

This handler prints the received message.
Returns None

##### `noCallback_handler(self, addr, tags, data, client_address)`

Example handler for OSCMessages.
All registerd handlers must accept these three arguments:
- addr (string): The OSC-address pattern of the received Message
  (the 'addr' string has already been matched against the handler's registerd OSC-address,
  but may contain '*'s & such)
- tags (string):  The OSC-typetags of the received message's arguments. (without the preceding comma)
- data (list): The OSCMessage's arguments
  Note that len(tags) == len(data)
- client_address ((host, port) tuple): the host & port this message originated from.

a Message-handler function may return None, but it could also return an OSCMessage (or OSCBundle),
which then gets sent back to the client.

This handler prints a "No callback registered to handle ..." message.
Returns None

##### `printErr(self, txt)`

Writes 'OSCServer: txt' to sys.stderr
                

##### `process_request(self, request, client_address)`

Start a new thread to process the request.

##### `process_request_thread(self, request, client_address)`

Same as in BaseServer but as a thread.

In addition, exception handling is done here.

##### `reportErr(self, txt, client_address)`

Writes 'OSCServer: txt' to sys.stderr
If self.error_prefix is defined, sends 'txt' as an OSC error-message to the client(s)
(see printErr() and sendOSCerror())

##### `sendOSCerror(self, txt, client_address)`

Sends 'txt', encapsulated in an OSCMessage to the default 'error_prefix' OSC-addres.
Message is sent to the given client_address, with the default 'return_port' overriding
the client_address' port, if defined.

##### `sendOSCinfo(self, txt, client_address)`

Sends 'txt', encapsulated in an OSCMessage to the default 'info_prefix' OSC-addres.
Message is sent to the given client_address, with the default 'return_port' overriding
the client_address' port, if defined.

##### `serve_forever(self)`

Handle one request at a time until server is closed.

##### `serverInfo_handler(self, addr, tags, data, client_address)`

Example handler for OSCMessages.
All registerd handlers must accept these three arguments:
- addr (string): The OSC-address pattern of the received Message
  (the 'addr' string has already been matched against the handler's registerd OSC-address,
  but may contain '*'s & such)
- tags (string):  The OSC-typetags of the received message's arguments. (without the preceding comma)
- data (list): The OSCMessage's arguments
  Note that len(tags) == len(data)
- client_address ((host, port) tuple): the host & port this message originated from.

a Message-handler function may return None, but it could also return an OSCMessage (or OSCBundle),
which then gets sent back to the client.

This handler returns a reply to the client, which can contain various bits of information
about this server, depending on the first argument of the received OSC-message:
- 'help' | 'info' :  Reply contains server type & version info, plus a list of 
  available 'commands' understood by this handler
- 'list' | 'ls' :  Reply is a bundle of 'address <string>' messages, listing the server's 
  OSC address-space.
- 'clients' | 'targets' :  Reply is a bundle of 'target osc://<host>:<port>[<prefix>] [<filter>] [...]'
  messages, listing the local Client-instance's subscribed remote clients.

##### `server_activate(self)`

Called by constructor to activate the server.

May be overridden.

##### `server_bind(self)`

Called by constructor to bind the socket.

May be overridden.

##### `server_close(self)`

Called to clean-up the server.

May be overridden.

##### `service_actions(self)`

Called by the serve_forever() loop.

May be overridden by a subclass / Mixin to implement any code that
needs to be run during the loop.

##### `setClient(self, client)`

Associate this Server with a new local Client instance, closing the Client this Server is currently using.
                

##### `setReturnPort(self, port)`

Set the destination UDP-port for replies returning from this server to the remote client
                

##### `setSrvErrorPrefix(self, pattern=)`

Set the OSC-address (pattern) this server will use to report errors occuring during
received message handling to the remote client.

If pattern is empty (default), server-errors are not reported back to the client.

##### `setSrvInfoPrefix(self, pattern)`

Set the first part of OSC-address (pattern) this server will use to reply to server-info requests.
                

##### `shutdown(self)`

Stops the serve_forever loop.

Blocks until the loop has finished. This must be called while
serve_forever() is running in another thread, or it will
deadlock.

##### `shutdown_request(self, request)`

Called to shutdown and close an individual request.

##### `subscription_handler(self, addr, tags, data, client_address)`

Handle 'subscribe' / 'unsubscribe' requests from remote hosts,
if the local Client supports this (i.e. OSCMultiClient).

Supported commands:
- 'help' | 'info' :  Reply contains server type & version info, plus a list of 
  available 'commands' understood by this handler
- 'list' | 'ls' :  Reply is a bundle of 'target osc://<host>:<port>[<prefix>] [<filter>] [...]'
  messages, listing the local Client-instance's subscribed remote clients.
- '[subscribe | listen | sendto | target] <url> [<filter> ...] :  Subscribe remote client/server at <url>,
  and/or set message-filters for messages being sent to the subscribed host, with the optional <filter>
  arguments. Filters are given as OSC-addresses (or '*') prefixed by a '+' (send matching messages) or
  a '-' (don't send matching messages). The wildcard '*', '+*' or '+/*' means 'send all' / 'filter none',
  and '-*' or '-/*' means 'send none' / 'filter all' (which is not the same as unsubscribing!)
  Reply is an OSCMessage with the (new) subscription; 'target osc://<host>:<port>[<prefix>] [<filter>] [...]' 
- '[unsubscribe | silence | nosend | deltarget] <url> :  Unsubscribe remote client/server at <url>
  If the given <url> isn't subscribed, a NotSubscribedError-message is printed (and possibly sent)

The <url> given to the subscribe/unsubscribe handler should be of the form:
'[osc://][<host>][:<port>][<prefix>]', where any or all components can be omitted.

If <host> is not specified, the IP-address of the message's source is used.
If <port> is not specified, the <host> is first looked up in the list of subscribed hosts, and if found,
the associated port is used.
If <port> is not specified and <host> is not yet subscribed, the message's source-port is used.
If <prefix> is specified on subscription, <prefix> is prepended to the OSC-address of all messages
sent to the subscribed host.
If <prefix> is specified on unsubscription, the subscribed host is only unsubscribed if the host, 
port and prefix all match the subscription.
If <prefix> is not specified on unsubscription, the subscribed host is unsubscribed if the host and port 
match the subscription.

##### `verify_request(self, request, client_address)`

Verify the request.  May be overridden.

Return True if we should proceed with this request.

---

### `NoCallbackError(self, pattern)`

This error is raised (by an OSCServer) when an OSCMessage with an 'unmatched' address-pattern
is received, and no 'default' handler is registered.

#### Methods

##### `__init__(self, pattern)`

The specified 'pattern' should be the OSC-address of the 'unmatched' message causing the error to be raised.
                

##### `__str__(self)`

Return str(self).

---

### `NotSubscribedError(self, addr, prefix=None)`

This error is raised (by an OSCMultiClient) when an attempt is made to unsubscribe a host
that isn't subscribed.

#### Methods

##### `__init__(self, addr, prefix=None)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__str__(self)`

Return str(self).

---

### `OSCAddressSpace(self)`



#### Methods

##### `__init__(self)`

Initialize self.  See help(type(self)) for accurate signature.

##### `addMsgHandler(self, address, callback)`

Register a handler for an OSC-address
  - 'address' is the OSC address-string. 
the address-string should start with '/' and may not contain '*'
  - 'callback' is the function called for incoming OSCMessages that match 'address'.
The callback-function will be called with the same arguments as the 'msgPrinter_handler' below

##### `delMsgHandler(self, address)`

Remove the registered handler for the given OSC-address
                

##### `dispatchMessage(self, pattern, tags, data, client_address)`

Attmept to match the given OSC-address pattern, which may contain '*',
against all callbacks registered with the OSCServer.
Calls the matching callback and returns whatever it returns.
If no match is found, and a 'default' callback is registered, it calls that one,
or raises NoCallbackError if a 'default' callback is not registered.

  - pattern (string):  The OSC-address of the receied message
  - tags (string):  The OSC-typetags of the receied message's arguments, without ','
  - data (list):  The message arguments

##### `getOSCAddressSpace(self)`

Returns a list containing all OSC-addresses registerd with this Server. 
                

---

### `OSCBundle(self, address=, time=0)`

Builds a 'bundle' of OSC messages.

OSCBundle objects are container objects for building OSC-bundles of OSC-messages.
An OSC-bundle is a special kind of OSC-message which contains a list of OSC-messages
(And yes, OSC-bundles may contain other OSC-bundles...)

OSCBundle objects behave much the same as OSCMessage objects, with these exceptions:
  - if an item or items to be appended or inserted are not OSCMessage objects, 
  OSCMessage objectss are created to encapsulate the item(s)
  - an OSC-bundle does not have an address of its own, only the contained OSC-messages do.
  The OSCBundle's 'address' is inherited by any OSCMessage the OSCBundle object creates.
  - OSC-bundles have a timetag to tell the receiver when the bundle should be processed.
  The default timetag value (0) means 'immediately'

#### Methods

##### `__add__(self, values)`

Returns a copy of self, with the contents of 'values' appended
(see the 'extend()' method, below)

##### `__contains__(self, val)`

Test if the given value appears in the OSCMessage's arguments
                

##### `__delitem__(self, i)`

Removes the indicated argument (or slice)
                

##### `__eq__(self, other)`

Return True if two OSCBundles have the same timetag & content
                

##### `__getitem__(self, i)`

Returns the indicated argument (or slice)
                

##### `__iadd__(self, values)`

Appends the contents of 'values'
(equivalent to 'extend()', below)
Returns self

##### `__init__(self, address=, time=0)`

Instantiate a new OSCBundle.
The default OSC-address for newly created OSCMessages 
can be specified with the 'address' argument
The bundle's timetag can be set with the 'time' argument

##### `__iter__(self)`

Returns an iterator of the OSCMessage's arguments
                

##### `__len__(self)`

Returns the number of arguments appended so far
                

##### `__ne__(self, other)`

Return (not self.__eq__(other))
                

##### `__radd__(self, values)`

Appends the contents of this OSCMessage to 'values'
Returns the extended 'values' (list or tuple)

##### `__repr__(self)`

Returns a string containing the decode Message
                

##### `__reversed__(self)`

Returns a reverse iterator of the OSCMessage's arguments
                

##### `__setitem__(self, i, val)`

Set indicatated argument (or slice) to a new value.
'val' can be a single int/float/string, or a (typehint, value) tuple.
Or, if 'i' is a slice, a list of these or another OSCMessage.

##### `__str__(self)`

Returns the Bundle's contents (and timetag, if nonzero) as a string.
                

##### `_reencode(self, items)`

Erase & rebuild the OSCMessage contents from the given
list of (typehint, value) tuples

##### `append(self, argument, typehint=None)`

Appends data to the bundle, creating an OSCMessage to encapsulate
the provided argument unless this is already an OSCMessage.
Any newly created OSCMessage inherits the OSCBundle's address at the time of creation.
If 'argument' is an iterable, its elements will be encapsuated by a single OSCMessage.
Finally, 'argument' can be (or contain) a dict, which will be 'converted' to an OSCMessage;
  - if 'addr' appears in the dict, its value overrides the OSCBundle's address
  - if 'args' appears in the dict, its value(s) become the OSCMessage's arguments

##### `clear(self, address=)`

Clear (or set a new) OSC-address and clear any arguments appended so far
                

##### `clearData(self)`

Clear any arguments appended so far
                

##### `copy(self)`

Returns a deep copy of this OSCBundle
                

##### `count(self, val)`

Returns the number of times the given value occurs in the OSCMessage's arguments
                

##### `extend(self, values)`

Append the contents of 'values' to this OSCMessage.
'values' can be another OSCMessage, or a list/tuple of ints/floats/strings

##### `getBinary(self)`

Returns the binary representation of the message
                

##### `getTimeTagStr(self)`

Return the TimeTag as a human-readable string
                

##### `index(self, val)`

Returns the index of the first occurence of the given value in the OSCMessage's arguments.
Raises ValueError if val isn't found

##### `insert(self, i, val, typehint=None)`

Insert given value (with optional typehint) into the OSCMessage
at the given index.

##### `items(self)`

Returns a list of (typetag, value) tuples for 
the arguments appended so far

##### `iteritems(self)`

Returns an iterator of the OSCMessage's arguments as
(typetag, value) tuples

##### `itertags(self)`

Returns an iterator of the OSCMessage's arguments' typetags
                

##### `itervalues(self)`

Returns an iterator of the OSCMessage's arguments
                

##### `pop(self, i)`

Delete the indicated argument from the OSCMessage, and return it.
                

##### `popitem(self, i)`

Delete the indicated argument from the OSCMessage, and return it
as a (typetag, value) tuple.

##### `remove(self, val)`

Removes the first argument with the given value from the OSCMessage.
Raises ValueError if val isn't found.

##### `reverse(self)`

Reverses the arguments of the OSCMessage (in place)
                

##### `setAddress(self, address)`

Set or change the OSC-address
                

##### `setItem(self, i, val, typehint=None)`

Set indicated argument to a new value (with typehint)
                

##### `setTimeTag(self, time)`

Set or change the OSCBundle's TimeTag
In 'Python Time', that's floating seconds since the Epoch

##### `tags(self)`

Returns a list of typetags of the appended arguments
                

##### `values(self)`

Returns a list of the OSCMessages appended so far
                

---

### `OSCClient(self, server=None)`

Simple OSC Client. Handles the sending of OSC-Packets (OSCMessage or OSCBundle) via a UDP-socket
        

#### Methods

##### `__eq__(self, other)`

Compare function.
                

##### `__init__(self, server=None)`

Construct an OSC Client.
- server: Local OSCServer-instance this client will use the socket of for transmissions.
If none is supplied, a socket will be created.

##### `__ne__(self, other)`

Compare function.
                

##### `__str__(self)`

Returns a string containing this Client's Class-name, software-version
and the remote-address it is connected to (if any)

##### `_ensureConnected(self, address)`

Make sure client has a socket connected to address

##### `_setSocket(self, skt)`

Set and configure client socket

##### `address(self)`

Returns a (host,port) tuple of the remote server this client is
connected to or None if not connected to any server.

##### `close(self)`

Disconnect & close the Client's socket
                

##### `connect(self, address)`

Bind to a specific OSC server:
the 'address' argument is a (host, port) tuple
  - host:  hostname of the remote OSC server,
  - port:  UDP-port the remote OSC server listens to.

##### `send(self, msg, timeout=None)`

Send the given OSCMessage.
The Client must be already connected.
  - msg:  OSCMessage (or OSCBundle) to be sent
  - timeout:  A timeout value for attempting to send. If timeout == None,
        this call blocks until socket is available for writing. 
Raises OSCClientError when timing out while waiting for the socket,
or when the Client isn't connected to a remote server.

##### `sendto(self, msg, address, timeout=None)`

Send the given OSCMessage to the specified address.
  - msg:  OSCMessage (or OSCBundle) to be sent
  - address:  (host, port) tuple specifing remote server to send the message to
  - timeout:  A timeout value for attempting to send. If timeout == None,
        this call blocks until socket is available for writing. 
Raises OSCClientError when timing out while waiting for the socket. 

##### `setServer(self, server)`

Associate this Client with given server.
The Client will send from the Server's socket.
The Server will use this Client instance to send replies.

---

### `OSCClientError(self, message)`

Class for all OSCClient errors
        

#### Methods

##### `__init__(self, message)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__str__(self)`

Return str(self).

---

### `OSCError(self, message)`

Base Class for all OSC-related errors
        

#### Methods

##### `__init__(self, message)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__str__(self)`

Return str(self).

---

### `OSCMessage(self, address=, *args)`

Builds typetagged OSC messages. 

OSCMessage objects are container objects for building OSC-messages.
On the 'front' end, they behave much like list-objects, and on the 'back' end
they generate a binary representation of the message, which can be sent over a network socket.
OSC-messages consist of an 'address'-string (not to be confused with a (host, port) IP-address!),
followed by a string of 'typetags' associated with the message's arguments (ie. 'payload'), 
and finally the arguments themselves, encoded in an OSC-specific way.

On the Python end, OSCMessage are lists of arguments, prepended by the message's address.
The message contents can be manipulated much like a list:
  >>> msg = OSCMessage("/my/osc/address")
  >>> msg.append('something')
  >>> msg.insert(0, 'something else')
  >>> msg[1] = 'entirely'
  >>> msg.extend([1,2,3.])
  >>> msg += [4, 5, 6.]
  >>> del msg[3:6]
  >>> msg.pop(-2)
  5
  >>> print msg
  /my/osc/address ['something else', 'entirely', 1, 6.0]

OSCMessages can be concatenated with the + operator. In this case, the resulting OSCMessage
inherits its address from the left-hand operand. The right-hand operand's address is ignored.
To construct an 'OSC-bundle' from multiple OSCMessage, see OSCBundle!

Additional methods exist for retreiving typetags or manipulating items as (typetag, value) tuples.

#### Methods

##### `__add__(self, values)`

Returns a copy of self, with the contents of 'values' appended
(see the 'extend()' method, below)

##### `__contains__(self, val)`

Test if the given value appears in the OSCMessage's arguments
                

##### `__delitem__(self, i)`

Removes the indicated argument (or slice)
                

##### `__eq__(self, other)`

Return True if two OSCMessages have the same address & content
                

##### `__getitem__(self, i)`

Returns the indicated argument (or slice)
                

##### `__iadd__(self, values)`

Appends the contents of 'values'
(equivalent to 'extend()', below)
Returns self

##### `__init__(self, address=, *args)`

Instantiate a new OSCMessage.
The OSC-address can be specified with the 'address' argument.
The rest of the arguments are appended as data.

##### `__iter__(self)`

Returns an iterator of the OSCMessage's arguments
                

##### `__len__(self)`

Returns the number of arguments appended so far
                

##### `__ne__(self, other)`

Return (not self.__eq__(other))
                

##### `__radd__(self, values)`

Appends the contents of this OSCMessage to 'values'
Returns the extended 'values' (list or tuple)

##### `__repr__(self)`

Returns a string containing the decode Message
                

##### `__reversed__(self)`

Returns a reverse iterator of the OSCMessage's arguments
                

##### `__setitem__(self, i, val)`

Set indicatated argument (or slice) to a new value.
'val' can be a single int/float/string, or a (typehint, value) tuple.
Or, if 'i' is a slice, a list of these or another OSCMessage.

##### `__str__(self)`

Returns the Message's address and contents as a string.
                

##### `_reencode(self, items)`

Erase & rebuild the OSCMessage contents from the given
list of (typehint, value) tuples

##### `append(self, argument, typehint=None)`

Appends data to the message, updating the typetags based on
the argument's type. If the argument is a blob (counted
string) pass in 'b' as typehint.
'argument' may also be a list or tuple, in which case its elements
will get appended one-by-one, all using the provided typehint

##### `clear(self, address=)`

Clear (or set a new) OSC-address and clear any arguments appended so far
                

##### `clearData(self)`

Clear any arguments appended so far
                

##### `copy(self)`

Returns a deep copy of this OSCMessage
                

##### `count(self, val)`

Returns the number of times the given value occurs in the OSCMessage's arguments
                

##### `extend(self, values)`

Append the contents of 'values' to this OSCMessage.
'values' can be another OSCMessage, or a list/tuple of ints/floats/strings

##### `getBinary(self)`

Returns the binary representation of the message
                

##### `index(self, val)`

Returns the index of the first occurence of the given value in the OSCMessage's arguments.
Raises ValueError if val isn't found

##### `insert(self, i, val, typehint=None)`

Insert given value (with optional typehint) into the OSCMessage
at the given index.

##### `items(self)`

Returns a list of (typetag, value) tuples for 
the arguments appended so far

##### `iteritems(self)`

Returns an iterator of the OSCMessage's arguments as
(typetag, value) tuples

##### `itertags(self)`

Returns an iterator of the OSCMessage's arguments' typetags
                

##### `itervalues(self)`

Returns an iterator of the OSCMessage's arguments
                

##### `pop(self, i)`

Delete the indicated argument from the OSCMessage, and return it.
                

##### `popitem(self, i)`

Delete the indicated argument from the OSCMessage, and return it
as a (typetag, value) tuple.

##### `remove(self, val)`

Removes the first argument with the given value from the OSCMessage.
Raises ValueError if val isn't found.

##### `reverse(self)`

Reverses the arguments of the OSCMessage (in place)
                

##### `setAddress(self, address)`

Set or change the OSC-address
                

##### `setItem(self, i, val, typehint=None)`

Set indicated argument to a new value (with typehint)
                

##### `tags(self)`

Returns a list of typetags of the appended arguments
                

##### `values(self)`

Returns a list of the arguments appended so far
                

---

### `OSCMultiClient(self, server=None)`

'Multiple-Unicast' OSC Client. Handles the sending of OSC-Packets (OSCMessage or OSCBundle) via a UDP-socket
This client keeps a dict of 'OSCTargets'. and sends each OSCMessage to each OSCTarget
The OSCTargets are simply (host, port) tuples, and may be associated with an OSC-address prefix.
the OSCTarget's prefix gets prepended to each OSCMessage sent to that target.

#### Methods

##### `__eq__(self, other)`

Compare function.
                

##### `__init__(self, server=None)`

Construct a "Multi" OSC Client.
- server: Local OSCServer-instance this client will use the socket of for transmissions.
If none is supplied, a socket will be created.

##### `__ne__(self, other)`

Compare function.
                

##### `__str__(self)`

Returns a string containing this Client's Class-name, software-version
and the remote-address it is connected to (if any)

##### `_delTarget(self, address, prefix=None)`

Delete the specified OSCTarget from the Client's dict.
the 'address' argument must be a (host, port) tuple.
If the 'prefix' argument is given, the Target is only deleted if the address and prefix match.

##### `_ensureConnected(self, address)`

Make sure client has a socket connected to address

##### `_filterMessage(self, filters, msg)`

Checks the given OSCMessge against the given filters.
'filters' is a dict containing OSC-address:bool pairs.
If 'msg' is an OSCBundle, recursively filters its constituents. 
Returns None if the message is to be filtered, else returns the message.
or
Returns a copy of the OSCBundle with the filtered messages removed.

##### `_prefixAddress(self, prefix, msg)`

Makes a copy of the given OSCMessage, then prepends the given prefix to
The message's OSC-address.
If 'msg' is an OSCBundle, recursively prepends the prefix to its constituents. 

##### `_searchHostAddr(self, host)`

Search the subscribed OSCTargets for (the first occurence of) given host.
Returns a (host, port) tuple

##### `_setSocket(self, skt)`

Set and configure client socket

##### `_setTarget(self, address, prefix=None, filters=None)`

Add (i.e. subscribe) a new OSCTarget, or change the prefix for an existing OSCTarget.
  - address ((host, port) tuple): IP-address & UDP-port 
  - prefix (string): The OSC-address prefix prepended to the address of each OSCMessage
sent to this OSCTarget (optional)

##### `_updateFilters(self, dst, src)`

Update a 'filters' dict with values form another 'filters' dict:
- src[a] == True and dst[a] == False:  del dst[a]
- src[a] == False and dst[a] == True:  del dst[a]
- a not in dst:  dst[a] == src[a]

##### `address(self)`

Returns a (host,port) tuple of the remote server this client is
connected to or None if not connected to any server.

##### `clearOSCTargets(self)`

Erases all OSCTargets from the Client's dict
                

##### `close(self)`

Disconnect & close the Client's socket
                

##### `connect(self, address)`

The OSCMultiClient isn't allowed to connect to any specific
address.

##### `delOSCTarget(self, address, prefix=None)`

Delete the specified OSCTarget from the Client's dict.
the 'address' argument can be a ((host, port) tuple), or a hostname.
If the 'prefix' argument is given, the Target is only deleted if the address and prefix match.

##### `getOSCTarget(self, address)`

Returns the OSCTarget matching the given address as a ((host, port), [prefix, filters]) tuple.
'address' can be a (host, port) tuple, or a 'host' (string), in which case the first matching OSCTarget is returned
Returns (None, ['',{}]) if address not found.

##### `getOSCTargetStr(self, address)`

Returns the OSCTarget matching the given address as a ('osc://<host>:<port>[<prefix>]', ['<filter-string>', ...])' tuple.
'address' can be a (host, port) tuple, or a 'host' (string), in which case the first matching OSCTarget is returned
Returns (None, []) if address not found.

##### `getOSCTargetStrings(self)`

Returns a list of all OSCTargets as ('osc://<host>:<port>[<prefix>]', ['<filter-string>', ...])' tuples.
                

##### `getOSCTargets(self)`

Returns the dict of OSCTargets: {addr:[prefix, filters], ...}
                

##### `hasOSCTarget(self, address, prefix=None)`

Return True if the given OSCTarget exists in the Client's dict.
the 'address' argument can be a ((host, port) tuple), or a hostname.
If the 'prefix' argument is given, the return-value is only True if the address and prefix match.

##### `send(self, msg, timeout=None)`

Send the given OSCMessage to all subscribed OSCTargets
  - msg:  OSCMessage (or OSCBundle) to be sent
  - timeout:  A timeout value for attempting to send. If timeout == None,
        this call blocks until socket is available for writing. 
Raises OSCClientError when timing out while waiting for the socket.

##### `sendto(self, msg, address, timeout=None)`

Send the given OSCMessage.
The specified address is ignored. Instead this method calls send() to
send the message to all subscribed clients.
  - msg:  OSCMessage (or OSCBundle) to be sent
  - address:  (host, port) tuple specifing remote server to send the message to
  - timeout:  A timeout value for attempting to send. If timeout == None,
        this call blocks until socket is available for writing. 
Raises OSCClientError when timing out while waiting for the socket. 

##### `setOSCTarget(self, address, prefix=None, filters=None)`

Add (i.e. subscribe) a new OSCTarget, or change the prefix for an existing OSCTarget.
the 'address' argument can be a ((host, port) tuple) : The target server address & UDP-port
  or a 'host' (string) : The host will be looked-up 
- prefix (string): The OSC-address prefix prepended to the address of each OSCMessage
sent to this OSCTarget (optional)

##### `setOSCTargetFromStr(self, url)`

Adds or modifies a subscribed OSCTarget from the given string, which should be in the
'<host>:<port>[/<prefix>] [+/<filter>]|[-/<filter>] ...' format.

##### `setServer(self, server)`

Associate this Client with given server.
The Client will send from the Server's socket.
The Server will use this Client instance to send replies.

##### `updateOSCTargets(self, dict)`

Update the Client's OSCTargets dict with the contents of 'dict'
The given dict's items MUST be of the form
  { (host, port):[prefix, filters], ... }

---

### `OSCRequestHandler(self, request, client_address, server)`

RequestHandler class for the OSCServer
        

#### Methods

##### `__init__(self, request, client_address, server)`

Initialize self.  See help(type(self)) for accurate signature.

##### `_unbundle(self, decoded)`

Recursive bundle-unpacking function

##### `finish(self)`

Finish handling OSCMessage.
Send any reply returned by the callback(s) back to the originating client
as an OSCMessage or OSCBundle

##### `handle(self)`

Handle incoming OSCMessage
                

##### `setup(self)`

Prepare RequestHandler.
Unpacks request as (packet, source socket address)
Creates an empty list for replies.

---

### `OSCServer(self, server_address, client=None, return_port=0)`

A Synchronous OSCServer
Serves one request at-a-time, until the OSCServer is closed.
The OSC address-pattern is matched against a set of OSC-adresses
that have been registered to the server with a callback-function.
If the adress-pattern of the message machtes the registered address of a callback,
that function is called. 

#### Methods

##### `__eq__(self, other)`

Compare function.
                

##### `__init__(self, server_address, client=None, return_port=0)`

Instantiate an OSCServer.
- server_address ((host, port) tuple): the local host & UDP-port
the server listens on
- client (OSCClient instance): The OSCClient used to send replies from this server.
If none is supplied (default) an OSCClient will be created.
- return_port (int): if supplied, sets the default UDP destination-port
for replies coming from this server.

##### `__ne__(self, other)`

Compare function.
                

##### `__str__(self)`

Returns a string containing this Server's Class-name, software-version and local bound address (if any)
                

##### `_handle_request_noblock(self)`

Handle one request, without blocking.

I assume that selector.select() has returned that the socket is
readable before this function was called, so there should be no risk of
blocking in get_request().

##### `_subscribe(self, data, client_address)`

Handle the actual subscription. the provided 'data' is concatenated together to form a
'<host>:<port>[<prefix>] [<filter>] [...]' string, which is then passed to 
parseUrlStr() & parseFilterStr() to actually retreive <host>, <port>, etc.

This 'long way 'round' approach (almost) guarantees that the subscription works, 
regardless of how the bits of the <url> are encoded in 'data'. 

##### `_unsubscribe(self, data, client_address)`

Handle the actual unsubscription. the provided 'data' is concatenated together to form a
'<host>:<port>[<prefix>]' string, which is then passed to 
parseUrlStr() to actually retreive <host>, <port> & <prefix>.

This 'long way 'round' approach (almost) guarantees that the unsubscription works, 
regardless of how the bits of the <url> are encoded in 'data'. 

##### `addDefaultHandlers(self, prefix=, info_prefix=/info, error_prefix=/error)`

Register a default set of OSC-address handlers with this Server:
- 'default' ->  noCallback_handler
the given prefix is prepended to all other callbacks registered by this method:
- '<prefix><info_prefix' ->  serverInfo_handler
- '<prefix><error_prefix> ->  msgPrinter_handler
- '<prefix>/print' ->  msgPrinter_handler
and, if the used Client supports it;
- '<prefix>/subscribe' -> subscription_handler
- '<prefix>/unsubscribe' -> subscription_handler

Note: the given 'error_prefix' argument is also set as default 'error_prefix' for error-messages
*sent from* this server. This is ok, because error-messages generally do not elicit a reply from the receiver.

To do this with the serverInfo-prefixes would be a bad idea, because if a request received on '/info' (for example)
would send replies to '/info', this could potentially cause a never-ending loop of messages!
Do *not* set the 'info_prefix' here (for incoming serverinfo requests) to the same value as given to
the setSrvInfoPrefix() method (for *replies* to incoming serverinfo requests).
For example, use '/info' for incoming requests, and '/inforeply' or '/serverinfo' or even just '/print' as the 
info-reply prefix. 

##### `addMsgHandler(self, address, callback)`

Register a handler for an OSC-address
  - 'address' is the OSC address-string. 
the address-string should start with '/' and may not contain '*'
  - 'callback' is the function called for incoming OSCMessages that match 'address'.
The callback-function will be called with the same arguments as the 'msgPrinter_handler' below

##### `address(self)`

Returns a (host,port) tuple of the local address this server is bound to,
or None if not bound to any address.

##### `close(self)`

Stops serving requests, closes server (socket), closes used client
                

##### `close_request(self, request)`

Called to clean up an individual request.

##### `delMsgHandler(self, address)`

Remove the registered handler for the given OSC-address
                

##### `dispatchMessage(self, pattern, tags, data, client_address)`

Attmept to match the given OSC-address pattern, which may contain '*',
against all callbacks registered with the OSCServer.
Calls the matching callback and returns whatever it returns.
If no match is found, and a 'default' callback is registered, it calls that one,
or raises NoCallbackError if a 'default' callback is not registered.

  - pattern (string):  The OSC-address of the receied message
  - tags (string):  The OSC-typetags of the receied message's arguments, without ','
  - data (list):  The message arguments

##### `fileno(self)`

Return socket file number.

Interface required by selector.

##### `finish_request(self, request, client_address)`

Finish one request by instantiating RequestHandlerClass.

##### `getOSCAddressSpace(self)`

Returns a list containing all OSC-addresses registerd with this Server. 
                

##### `get_request(self)`

Get the request and client address from the socket.

May be overridden.

##### `handle_error(self, request, client_address)`

Handle an exception in the Server's callbacks gracefully.
Writes the error to sys.stderr and, if the error_prefix (see setSrvErrorPrefix()) is set,
sends the error-message as reply to the client

##### `handle_request(self)`

Handle one request, possibly blocking.

Respects self.timeout.

##### `handle_timeout(self)`

Called if no new request arrives within self.timeout.

Overridden by ForkingMixIn.

##### `msgPrinter_handler(self, addr, tags, data, client_address)`

Example handler for OSCMessages.
All registerd handlers must accept these three arguments:
- addr (string): The OSC-address pattern of the received Message
  (the 'addr' string has already been matched against the handler's registerd OSC-address,
  but may contain '*'s & such)
- tags (string):  The OSC-typetags of the received message's arguments. (without the preceding comma)
- data (list): The OSCMessage's arguments
  Note that len(tags) == len(data)
- client_address ((host, port) tuple): the host & port this message originated from.

a Message-handler function may return None, but it could also return an OSCMessage (or OSCBundle),
which then gets sent back to the client.

This handler prints the received message.
Returns None

##### `noCallback_handler(self, addr, tags, data, client_address)`

Example handler for OSCMessages.
All registerd handlers must accept these three arguments:
- addr (string): The OSC-address pattern of the received Message
  (the 'addr' string has already been matched against the handler's registerd OSC-address,
  but may contain '*'s & such)
- tags (string):  The OSC-typetags of the received message's arguments. (without the preceding comma)
- data (list): The OSCMessage's arguments
  Note that len(tags) == len(data)
- client_address ((host, port) tuple): the host & port this message originated from.

a Message-handler function may return None, but it could also return an OSCMessage (or OSCBundle),
which then gets sent back to the client.

This handler prints a "No callback registered to handle ..." message.
Returns None

##### `printErr(self, txt)`

Writes 'OSCServer: txt' to sys.stderr
                

##### `process_request(self, request, client_address)`

Call finish_request.

Overridden by ForkingMixIn and ThreadingMixIn.

##### `reportErr(self, txt, client_address)`

Writes 'OSCServer: txt' to sys.stderr
If self.error_prefix is defined, sends 'txt' as an OSC error-message to the client(s)
(see printErr() and sendOSCerror())

##### `sendOSCerror(self, txt, client_address)`

Sends 'txt', encapsulated in an OSCMessage to the default 'error_prefix' OSC-addres.
Message is sent to the given client_address, with the default 'return_port' overriding
the client_address' port, if defined.

##### `sendOSCinfo(self, txt, client_address)`

Sends 'txt', encapsulated in an OSCMessage to the default 'info_prefix' OSC-addres.
Message is sent to the given client_address, with the default 'return_port' overriding
the client_address' port, if defined.

##### `serve_forever(self)`

Handle one request at a time until server is closed.

##### `serverInfo_handler(self, addr, tags, data, client_address)`

Example handler for OSCMessages.
All registerd handlers must accept these three arguments:
- addr (string): The OSC-address pattern of the received Message
  (the 'addr' string has already been matched against the handler's registerd OSC-address,
  but may contain '*'s & such)
- tags (string):  The OSC-typetags of the received message's arguments. (without the preceding comma)
- data (list): The OSCMessage's arguments
  Note that len(tags) == len(data)
- client_address ((host, port) tuple): the host & port this message originated from.

a Message-handler function may return None, but it could also return an OSCMessage (or OSCBundle),
which then gets sent back to the client.

This handler returns a reply to the client, which can contain various bits of information
about this server, depending on the first argument of the received OSC-message:
- 'help' | 'info' :  Reply contains server type & version info, plus a list of 
  available 'commands' understood by this handler
- 'list' | 'ls' :  Reply is a bundle of 'address <string>' messages, listing the server's 
  OSC address-space.
- 'clients' | 'targets' :  Reply is a bundle of 'target osc://<host>:<port>[<prefix>] [<filter>] [...]'
  messages, listing the local Client-instance's subscribed remote clients.

##### `server_activate(self)`

Called by constructor to activate the server.

May be overridden.

##### `server_bind(self)`

Called by constructor to bind the socket.

May be overridden.

##### `server_close(self)`

Called to clean-up the server.

May be overridden.

##### `service_actions(self)`

Called by the serve_forever() loop.

May be overridden by a subclass / Mixin to implement any code that
needs to be run during the loop.

##### `setClient(self, client)`

Associate this Server with a new local Client instance, closing the Client this Server is currently using.
                

##### `setReturnPort(self, port)`

Set the destination UDP-port for replies returning from this server to the remote client
                

##### `setSrvErrorPrefix(self, pattern=)`

Set the OSC-address (pattern) this server will use to report errors occuring during
received message handling to the remote client.

If pattern is empty (default), server-errors are not reported back to the client.

##### `setSrvInfoPrefix(self, pattern)`

Set the first part of OSC-address (pattern) this server will use to reply to server-info requests.
                

##### `shutdown(self)`

Stops the serve_forever loop.

Blocks until the loop has finished. This must be called while
serve_forever() is running in another thread, or it will
deadlock.

##### `shutdown_request(self, request)`

Called to shutdown and close an individual request.

##### `subscription_handler(self, addr, tags, data, client_address)`

Handle 'subscribe' / 'unsubscribe' requests from remote hosts,
if the local Client supports this (i.e. OSCMultiClient).

Supported commands:
- 'help' | 'info' :  Reply contains server type & version info, plus a list of 
  available 'commands' understood by this handler
- 'list' | 'ls' :  Reply is a bundle of 'target osc://<host>:<port>[<prefix>] [<filter>] [...]'
  messages, listing the local Client-instance's subscribed remote clients.
- '[subscribe | listen | sendto | target] <url> [<filter> ...] :  Subscribe remote client/server at <url>,
  and/or set message-filters for messages being sent to the subscribed host, with the optional <filter>
  arguments. Filters are given as OSC-addresses (or '*') prefixed by a '+' (send matching messages) or
  a '-' (don't send matching messages). The wildcard '*', '+*' or '+/*' means 'send all' / 'filter none',
  and '-*' or '-/*' means 'send none' / 'filter all' (which is not the same as unsubscribing!)
  Reply is an OSCMessage with the (new) subscription; 'target osc://<host>:<port>[<prefix>] [<filter>] [...]' 
- '[unsubscribe | silence | nosend | deltarget] <url> :  Unsubscribe remote client/server at <url>
  If the given <url> isn't subscribed, a NotSubscribedError-message is printed (and possibly sent)

The <url> given to the subscribe/unsubscribe handler should be of the form:
'[osc://][<host>][:<port>][<prefix>]', where any or all components can be omitted.

If <host> is not specified, the IP-address of the message's source is used.
If <port> is not specified, the <host> is first looked up in the list of subscribed hosts, and if found,
the associated port is used.
If <port> is not specified and <host> is not yet subscribed, the message's source-port is used.
If <prefix> is specified on subscription, <prefix> is prepended to the OSC-address of all messages
sent to the subscribed host.
If <prefix> is specified on unsubscription, the subscribed host is only unsubscribed if the host, 
port and prefix all match the subscription.
If <prefix> is not specified on unsubscription, the subscribed host is unsubscribed if the host and port 
match the subscription.

##### `verify_request(self, request, client_address)`

Verify the request.  May be overridden.

Return True if we should proceed with this request.

---

### `OSCServerError(self, message)`

Class for all OSCServer errors
        

#### Methods

##### `__init__(self, message)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__str__(self)`

Return str(self).

---

### `OSCStreamRequestHandler(self, request, client_address, server)`

This is the central class of a streaming OSC server. If a client
connects to the server, the server instantiates a OSCStreamRequestHandler
for each new connection. This is fundamentally different to a packet
oriented server which has a single address space for all connections.
This connection based (streaming) OSC server maintains an address space
for each single connection, because usually tcp server spawn a new thread
or process for each new connection. This would generate severe
multithreading synchronization problems when each thread would operate on
the same address space object. Therefore: To implement a streaming/TCP OSC
server a custom handler must be implemented which implements the
setupAddressSpace member in which it creates its own address space for this
very connection. This has been done within the testbench and can serve as
inspiration.

#### Methods

##### `__init__(self, request, client_address, server)`

Initialize all base classes. The address space must be initialized
before the stream request handler because the initialization function
of the stream request handler calls the setup member which again
requires an already initialized address space.

##### `_receive(self, count)`

Receive a certain amount of data from the socket and return it. If the
remote end should be closed in the meanwhile None is returned.

##### `_receiveMsg(self)`

Receive OSC message from a socket and decode.
If an error occurs, None is returned, else the message.

##### `_transmitMsg(self, msg)`

Send an OSC message over a streaming socket. Raises exception if it
should fail. If everything is transmitted properly, True is returned. If
socket has been closed, False.

##### `_unbundle(self, decoded)`

Recursive bundle-unpacking function

##### `addMsgHandler(self, address, callback)`

Register a handler for an OSC-address
  - 'address' is the OSC address-string. 
the address-string should start with '/' and may not contain '*'
  - 'callback' is the function called for incoming OSCMessages that match 'address'.
The callback-function will be called with the same arguments as the 'msgPrinter_handler' below

##### `delMsgHandler(self, address)`

Remove the registered handler for the given OSC-address
                

##### `dispatchMessage(self, pattern, tags, data, client_address)`

Attmept to match the given OSC-address pattern, which may contain '*',
against all callbacks registered with the OSCServer.
Calls the matching callback and returns whatever it returns.
If no match is found, and a 'default' callback is registered, it calls that one,
or raises NoCallbackError if a 'default' callback is not registered.

  - pattern (string):  The OSC-address of the receied message
  - tags (string):  The OSC-typetags of the receied message's arguments, without ','
  - data (list):  The message arguments

##### `getOSCAddressSpace(self)`

Returns a list containing all OSC-addresses registerd with this Server. 
                

##### `handle(self)`

Handle a connection.

##### `sendOSC(self, oscData)`

This member can be used to transmit OSC messages or OSC bundles
over the client/server connection. It is thread save.

##### `setupAddressSpace(self)`

Override this function to customize your address space. 

---

### `OSCStreamingClient(self)`

OSC streaming client.
A streaming client establishes a connection to a streaming server but must
be able to handle replies by the server as well. To accomplish this the
receiving takes place in a secondary thread, because no one knows if we
have to expect a reply or not, i.e. synchronous architecture doesn't make
much sense.
Replies will be matched against the local address space. If message
handlers access code of the main thread (where the client messages are sent
to the server) care must be taken e.g. by installing sychronization
mechanisms or by using an event dispatcher which can handle events
originating from other threads. 

#### Methods

##### `__eq__(self, other)`

Compare function.
                

##### `__init__(self)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__ne__(self, other)`

Compare function.
                

##### `__str__(self)`

Returns a string containing this Client's Class-name, software-version
and the remote-address it is connected to (if any)

##### `_receiveMsgWithTimeout(self)`

Receive OSC message from a socket and decode.
If an error occurs, None is returned, else the message.

##### `addMsgHandler(self, address, callback)`

Register a handler for an OSC-address
  - 'address' is the OSC address-string. 
the address-string should start with '/' and may not contain '*'
  - 'callback' is the function called for incoming OSCMessages that match 'address'.
The callback-function will be called with the same arguments as the 'msgPrinter_handler' below

##### `delMsgHandler(self, address)`

Remove the registered handler for the given OSC-address
                

##### `dispatchMessage(self, pattern, tags, data, client_address)`

Attmept to match the given OSC-address pattern, which may contain '*',
against all callbacks registered with the OSCServer.
Calls the matching callback and returns whatever it returns.
If no match is found, and a 'default' callback is registered, it calls that one,
or raises NoCallbackError if a 'default' callback is not registered.

  - pattern (string):  The OSC-address of the receied message
  - tags (string):  The OSC-typetags of the receied message's arguments, without ','
  - data (list):  The message arguments

##### `getOSCAddressSpace(self)`

Returns a list containing all OSC-addresses registerd with this Server. 
                

##### `sendOSC(self, msg)`

Send an OSC message or bundle to the server. Returns True on success.
                

---

### `OSCStreamingServer(self, address)`

A connection oriented (TCP/IP) OSC server.
        

#### Methods

##### `__init__(self, address)`

Instantiate an OSCStreamingServer.
- server_address ((host, port) tuple): the local host & UDP-port
the server listens for new connections.

##### `_clientRegister(self, client)`

Gets called by each request/connection handler when connection is
established to add itself to the client list

##### `_clientUnregister(self, client)`

Gets called by each request/connection handler when connection is
lost to remove itself from the client list

##### `_handle_request_noblock(self)`

Handle one request, without blocking.

I assume that selector.select() has returned that the socket is
readable before this function was called, so there should be no risk of
blocking in get_request().

##### `broadcastToClients(self, oscData)`

Send OSC message or bundle to all connected clients. 

##### `close_request(self, request)`

Called to clean up an individual request.

##### `fileno(self)`

Return socket file number.

Interface required by selector.

##### `finish_request(self, request, client_address)`

Finish one request by instantiating RequestHandlerClass.

##### `get_request(self)`

Get the request and client address from the socket.

May be overridden.

##### `handle_error(self, request, client_address)`

Handle an error gracefully.  May be overridden.

The default is to print a traceback and continue.

##### `handle_request(self)`

Handle one request, possibly blocking.

Respects self.timeout.

##### `handle_timeout(self)`

Called if no new request arrives within self.timeout.

Overridden by ForkingMixIn.

##### `process_request(self, request, client_address)`

Call finish_request.

Overridden by ForkingMixIn and ThreadingMixIn.

##### `serve_forever(self)`

Handle one request at a time until server is closed.
Had to add this since 2.5 does not support server.shutdown()

##### `server_activate(self)`

Called by constructor to activate the server.

May be overridden.

##### `server_bind(self)`

Called by constructor to bind the socket.

May be overridden.

##### `server_close(self)`

Called to clean-up the server.

May be overridden.

##### `service_actions(self)`

Called by the serve_forever() loop.

May be overridden by a subclass / Mixin to implement any code that
needs to be run during the loop.

##### `shutdown(self)`

Stops the serve_forever loop.

Blocks until the loop has finished. This must be called while
serve_forever() is running in another thread, or it will
deadlock.

##### `shutdown_request(self, request)`

Called to shutdown and close an individual request.

##### `start(self)`

Start the server thread. 

##### `stop(self)`

Stop the server thread and close the socket. 

##### `verify_request(self, request, client_address)`

Verify the request.  May be overridden.

Return True if we should proceed with this request.

---

### `OSCStreamingServerThreading(self, address)`

Mix-in class to handle each request in a new thread.

#### Methods

##### `__init__(self, address)`

Instantiate an OSCStreamingServer.
- server_address ((host, port) tuple): the local host & UDP-port
the server listens for new connections.

##### `_clientRegister(self, client)`

Gets called by each request/connection handler when connection is
established to add itself to the client list

##### `_clientUnregister(self, client)`

Gets called by each request/connection handler when connection is
lost to remove itself from the client list

##### `_handle_request_noblock(self)`

Handle one request, without blocking.

I assume that selector.select() has returned that the socket is
readable before this function was called, so there should be no risk of
blocking in get_request().

##### `broadcastToClients(self, oscData)`

Send OSC message or bundle to all connected clients. 

##### `close_request(self, request)`

Called to clean up an individual request.

##### `fileno(self)`

Return socket file number.

Interface required by selector.

##### `finish_request(self, request, client_address)`

Finish one request by instantiating RequestHandlerClass.

##### `get_request(self)`

Get the request and client address from the socket.

May be overridden.

##### `handle_error(self, request, client_address)`

Handle an error gracefully.  May be overridden.

The default is to print a traceback and continue.

##### `handle_request(self)`

Handle one request, possibly blocking.

Respects self.timeout.

##### `handle_timeout(self)`

Called if no new request arrives within self.timeout.

Overridden by ForkingMixIn.

##### `process_request(self, request, client_address)`

Start a new thread to process the request.

##### `process_request_thread(self, request, client_address)`

Same as in BaseServer but as a thread.

In addition, exception handling is done here.

##### `serve_forever(self)`

Handle one request at a time until server is closed.
Had to add this since 2.5 does not support server.shutdown()

##### `server_activate(self)`

Called by constructor to activate the server.

May be overridden.

##### `server_bind(self)`

Called by constructor to bind the socket.

May be overridden.

##### `server_close(self)`

Called to clean-up the server.

May be overridden.

##### `service_actions(self)`

Called by the serve_forever() loop.

May be overridden by a subclass / Mixin to implement any code that
needs to be run during the loop.

##### `shutdown(self)`

Stops the serve_forever loop.

Blocks until the loop has finished. This must be called while
serve_forever() is running in another thread, or it will
deadlock.

##### `shutdown_request(self, request)`

Called to shutdown and close an individual request.

##### `start(self)`

Start the server thread. 

##### `stop(self)`

Stop the server thread and close the socket. 

##### `verify_request(self, request, client_address)`

Verify the request.  May be overridden.

Return True if we should proceed with this request.

---

### `ThreadingOSCRequestHandler(self, request, client_address, server)`

Multi-threaded OSCRequestHandler;
Starts a new RequestHandler thread for each unbundled OSCMessage

#### Methods

##### `__init__(self, request, client_address, server)`

Initialize self.  See help(type(self)) for accurate signature.

##### `_unbundle(self, decoded)`

Recursive bundle-unpacking function
This version starts a new thread for each sub-Bundle found in the Bundle,
then waits for all its children to finish.

##### `finish(self)`

Finish handling OSCMessage.
Send any reply returned by the callback(s) back to the originating client
as an OSCMessage or OSCBundle

##### `handle(self)`

Handle incoming OSCMessage
                

##### `setup(self)`

Prepare RequestHandler.
Unpacks request as (packet, source socket address)
Creates an empty list for replies.

---

### `ThreadingOSCServer(self, server_address, client=None, return_port=0)`

An Asynchronous OSCServer.
This server starts a new thread to handle each incoming request.

#### Methods

##### `__eq__(self, other)`

Compare function.
                

##### `__init__(self, server_address, client=None, return_port=0)`

Instantiate an OSCServer.
- server_address ((host, port) tuple): the local host & UDP-port
the server listens on
- client (OSCClient instance): The OSCClient used to send replies from this server.
If none is supplied (default) an OSCClient will be created.
- return_port (int): if supplied, sets the default UDP destination-port
for replies coming from this server.

##### `__ne__(self, other)`

Compare function.
                

##### `__str__(self)`

Returns a string containing this Server's Class-name, software-version and local bound address (if any)
                

##### `_handle_request_noblock(self)`

Handle one request, without blocking.

I assume that selector.select() has returned that the socket is
readable before this function was called, so there should be no risk of
blocking in get_request().

##### `_subscribe(self, data, client_address)`

Handle the actual subscription. the provided 'data' is concatenated together to form a
'<host>:<port>[<prefix>] [<filter>] [...]' string, which is then passed to 
parseUrlStr() & parseFilterStr() to actually retreive <host>, <port>, etc.

This 'long way 'round' approach (almost) guarantees that the subscription works, 
regardless of how the bits of the <url> are encoded in 'data'. 

##### `_unsubscribe(self, data, client_address)`

Handle the actual unsubscription. the provided 'data' is concatenated together to form a
'<host>:<port>[<prefix>]' string, which is then passed to 
parseUrlStr() to actually retreive <host>, <port> & <prefix>.

This 'long way 'round' approach (almost) guarantees that the unsubscription works, 
regardless of how the bits of the <url> are encoded in 'data'. 

##### `addDefaultHandlers(self, prefix=, info_prefix=/info, error_prefix=/error)`

Register a default set of OSC-address handlers with this Server:
- 'default' ->  noCallback_handler
the given prefix is prepended to all other callbacks registered by this method:
- '<prefix><info_prefix' ->  serverInfo_handler
- '<prefix><error_prefix> ->  msgPrinter_handler
- '<prefix>/print' ->  msgPrinter_handler
and, if the used Client supports it;
- '<prefix>/subscribe' -> subscription_handler
- '<prefix>/unsubscribe' -> subscription_handler

Note: the given 'error_prefix' argument is also set as default 'error_prefix' for error-messages
*sent from* this server. This is ok, because error-messages generally do not elicit a reply from the receiver.

To do this with the serverInfo-prefixes would be a bad idea, because if a request received on '/info' (for example)
would send replies to '/info', this could potentially cause a never-ending loop of messages!
Do *not* set the 'info_prefix' here (for incoming serverinfo requests) to the same value as given to
the setSrvInfoPrefix() method (for *replies* to incoming serverinfo requests).
For example, use '/info' for incoming requests, and '/inforeply' or '/serverinfo' or even just '/print' as the 
info-reply prefix. 

##### `addMsgHandler(self, address, callback)`

Register a handler for an OSC-address
  - 'address' is the OSC address-string. 
the address-string should start with '/' and may not contain '*'
  - 'callback' is the function called for incoming OSCMessages that match 'address'.
The callback-function will be called with the same arguments as the 'msgPrinter_handler' below

##### `address(self)`

Returns a (host,port) tuple of the local address this server is bound to,
or None if not bound to any address.

##### `close(self)`

Stops serving requests, closes server (socket), closes used client
                

##### `close_request(self, request)`

Called to clean up an individual request.

##### `delMsgHandler(self, address)`

Remove the registered handler for the given OSC-address
                

##### `dispatchMessage(self, pattern, tags, data, client_address)`

Attmept to match the given OSC-address pattern, which may contain '*',
against all callbacks registered with the OSCServer.
Calls the matching callback and returns whatever it returns.
If no match is found, and a 'default' callback is registered, it calls that one,
or raises NoCallbackError if a 'default' callback is not registered.

  - pattern (string):  The OSC-address of the receied message
  - tags (string):  The OSC-typetags of the receied message's arguments, without ','
  - data (list):  The message arguments

##### `fileno(self)`

Return socket file number.

Interface required by selector.

##### `finish_request(self, request, client_address)`

Finish one request by instantiating RequestHandlerClass.

##### `getOSCAddressSpace(self)`

Returns a list containing all OSC-addresses registerd with this Server. 
                

##### `get_request(self)`

Get the request and client address from the socket.

May be overridden.

##### `handle_error(self, request, client_address)`

Handle an exception in the Server's callbacks gracefully.
Writes the error to sys.stderr and, if the error_prefix (see setSrvErrorPrefix()) is set,
sends the error-message as reply to the client

##### `handle_request(self)`

Handle one request, possibly blocking.

Respects self.timeout.

##### `handle_timeout(self)`

Called if no new request arrives within self.timeout.

Overridden by ForkingMixIn.

##### `msgPrinter_handler(self, addr, tags, data, client_address)`

Example handler for OSCMessages.
All registerd handlers must accept these three arguments:
- addr (string): The OSC-address pattern of the received Message
  (the 'addr' string has already been matched against the handler's registerd OSC-address,
  but may contain '*'s & such)
- tags (string):  The OSC-typetags of the received message's arguments. (without the preceding comma)
- data (list): The OSCMessage's arguments
  Note that len(tags) == len(data)
- client_address ((host, port) tuple): the host & port this message originated from.

a Message-handler function may return None, but it could also return an OSCMessage (or OSCBundle),
which then gets sent back to the client.

This handler prints the received message.
Returns None

##### `noCallback_handler(self, addr, tags, data, client_address)`

Example handler for OSCMessages.
All registerd handlers must accept these three arguments:
- addr (string): The OSC-address pattern of the received Message
  (the 'addr' string has already been matched against the handler's registerd OSC-address,
  but may contain '*'s & such)
- tags (string):  The OSC-typetags of the received message's arguments. (without the preceding comma)
- data (list): The OSCMessage's arguments
  Note that len(tags) == len(data)
- client_address ((host, port) tuple): the host & port this message originated from.

a Message-handler function may return None, but it could also return an OSCMessage (or OSCBundle),
which then gets sent back to the client.

This handler prints a "No callback registered to handle ..." message.
Returns None

##### `printErr(self, txt)`

Writes 'OSCServer: txt' to sys.stderr
                

##### `process_request(self, request, client_address)`

Start a new thread to process the request.

##### `process_request_thread(self, request, client_address)`

Same as in BaseServer but as a thread.

In addition, exception handling is done here.

##### `reportErr(self, txt, client_address)`

Writes 'OSCServer: txt' to sys.stderr
If self.error_prefix is defined, sends 'txt' as an OSC error-message to the client(s)
(see printErr() and sendOSCerror())

##### `sendOSCerror(self, txt, client_address)`

Sends 'txt', encapsulated in an OSCMessage to the default 'error_prefix' OSC-addres.
Message is sent to the given client_address, with the default 'return_port' overriding
the client_address' port, if defined.

##### `sendOSCinfo(self, txt, client_address)`

Sends 'txt', encapsulated in an OSCMessage to the default 'info_prefix' OSC-addres.
Message is sent to the given client_address, with the default 'return_port' overriding
the client_address' port, if defined.

##### `serve_forever(self)`

Handle one request at a time until server is closed.

##### `serverInfo_handler(self, addr, tags, data, client_address)`

Example handler for OSCMessages.
All registerd handlers must accept these three arguments:
- addr (string): The OSC-address pattern of the received Message
  (the 'addr' string has already been matched against the handler's registerd OSC-address,
  but may contain '*'s & such)
- tags (string):  The OSC-typetags of the received message's arguments. (without the preceding comma)
- data (list): The OSCMessage's arguments
  Note that len(tags) == len(data)
- client_address ((host, port) tuple): the host & port this message originated from.

a Message-handler function may return None, but it could also return an OSCMessage (or OSCBundle),
which then gets sent back to the client.

This handler returns a reply to the client, which can contain various bits of information
about this server, depending on the first argument of the received OSC-message:
- 'help' | 'info' :  Reply contains server type & version info, plus a list of 
  available 'commands' understood by this handler
- 'list' | 'ls' :  Reply is a bundle of 'address <string>' messages, listing the server's 
  OSC address-space.
- 'clients' | 'targets' :  Reply is a bundle of 'target osc://<host>:<port>[<prefix>] [<filter>] [...]'
  messages, listing the local Client-instance's subscribed remote clients.

##### `server_activate(self)`

Called by constructor to activate the server.

May be overridden.

##### `server_bind(self)`

Called by constructor to bind the socket.

May be overridden.

##### `server_close(self)`

Called to clean-up the server.

May be overridden.

##### `service_actions(self)`

Called by the serve_forever() loop.

May be overridden by a subclass / Mixin to implement any code that
needs to be run during the loop.

##### `setClient(self, client)`

Associate this Server with a new local Client instance, closing the Client this Server is currently using.
                

##### `setReturnPort(self, port)`

Set the destination UDP-port for replies returning from this server to the remote client
                

##### `setSrvErrorPrefix(self, pattern=)`

Set the OSC-address (pattern) this server will use to report errors occuring during
received message handling to the remote client.

If pattern is empty (default), server-errors are not reported back to the client.

##### `setSrvInfoPrefix(self, pattern)`

Set the first part of OSC-address (pattern) this server will use to reply to server-info requests.
                

##### `shutdown(self)`

Stops the serve_forever loop.

Blocks until the loop has finished. This must be called while
serve_forever() is running in another thread, or it will
deadlock.

##### `shutdown_request(self, request)`

Called to shutdown and close an individual request.

##### `subscription_handler(self, addr, tags, data, client_address)`

Handle 'subscribe' / 'unsubscribe' requests from remote hosts,
if the local Client supports this (i.e. OSCMultiClient).

Supported commands:
- 'help' | 'info' :  Reply contains server type & version info, plus a list of 
  available 'commands' understood by this handler
- 'list' | 'ls' :  Reply is a bundle of 'target osc://<host>:<port>[<prefix>] [<filter>] [...]'
  messages, listing the local Client-instance's subscribed remote clients.
- '[subscribe | listen | sendto | target] <url> [<filter> ...] :  Subscribe remote client/server at <url>,
  and/or set message-filters for messages being sent to the subscribed host, with the optional <filter>
  arguments. Filters are given as OSC-addresses (or '*') prefixed by a '+' (send matching messages) or
  a '-' (don't send matching messages). The wildcard '*', '+*' or '+/*' means 'send all' / 'filter none',
  and '-*' or '-/*' means 'send none' / 'filter all' (which is not the same as unsubscribing!)
  Reply is an OSCMessage with the (new) subscription; 'target osc://<host>:<port>[<prefix>] [<filter>] [...]' 
- '[unsubscribe | silence | nosend | deltarget] <url> :  Unsubscribe remote client/server at <url>
  If the given <url> isn't subscribed, a NotSubscribedError-message is printed (and possibly sent)

The <url> given to the subscribe/unsubscribe handler should be of the form:
'[osc://][<host>][:<port>][<prefix>]', where any or all components can be omitted.

If <host> is not specified, the IP-address of the message's source is used.
If <port> is not specified, the <host> is first looked up in the list of subscribed hosts, and if found,
the associated port is used.
If <port> is not specified and <host> is not yet subscribed, the message's source-port is used.
If <prefix> is specified on subscription, <prefix> is prepended to the OSC-address of all messages
sent to the subscribed host.
If <prefix> is specified on unsubscription, the subscribed host is only unsubscribed if the host, 
port and prefix all match the subscription.
If <prefix> is not specified on unsubscription, the subscribed host is unsubscribed if the host and port 
match the subscription.

##### `verify_request(self, request, client_address)`

Verify the request.  May be overridden.

Return True if we should proceed with this request.

---

## Functions

### `OSCArgument(next, typehint=None)`

Convert some Python types to their
OSC binary representations, returning a
(typetag, data) tuple.

### `OSCBlob(next)`

Convert a string into an OSC Blob.
An OSC-Blob is a binary encoded block of data, prepended by a 'size' (int32).
The size is always a mutiple of 4 bytes. 
The blob ends with 0 to 3 zero-bytes (' ') 

### `OSCString(next)`

Convert a string into a zero-padded OSC String.
The length of the resulting string is always a multiple of 4 bytes.
The string ends with 1 to 4 zero-bytes (' ') 

### `OSCTimeTag(time)`

Convert a time in floating seconds to its
OSC binary representation

### `_readBlob(data)`

Reads the next (numbered) block of data
        

### `_readDouble(data)`

Tries to interpret the next 8 bytes of the data
as a 64-bit float. 

### `_readFloat(data)`

Tries to interpret the next 4 bytes of the data
as a 32-bit float. 

### `_readInt(data)`

Tries to interpret the next 4 bytes of the data
as a 32-bit integer. 

### `_readLong(data)`

Tries to interpret the next 8 bytes of the data
as a 64-bit signed integer.
 

### `_readString(data)`

Reads the next (null-terminated) block of data
        

### `_readTimeTag(data)`

Tries to interpret the next 8 bytes of the data
as a TimeTag.
 

### `decodeOSC(data)`

Converts a binary OSC message to a Python list. 
        

### `getFilterStr(filters)`

Return the given 'filters' dict as a list of
'+<addr>' | '-<addr>' filter-strings

### `getRegEx(pattern)`

Compiles and returns a 'regular expression' object for the given address-pattern.
        

### `getUrlStr(*args)`

Convert provided arguments to a string in 'host:port/prefix' format
Args can be:
  - (host, port)
  - (host, port), prefix
  - host, port
  - host, port, prefix

### `hexDump(bytes)`

Useful utility; prints the string in hexadecimal.
        

### `parseFilterStr(args)`

Convert Message-Filter settings in '+<addr> -<addr> ...' format to a dict of the form
{ '<addr>':True, '<addr>':False, ... } 
Returns a list: ['<prefix>', filters]

### `parseUrlStr(url)`

Convert provided string in 'host:port/prefix' format to it's components
Returns ((host, port), prefix)

## Data

