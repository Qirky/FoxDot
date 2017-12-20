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

---

### `NoCallbackError(self, pattern)`

This error is raised (by an OSCServer) when an OSCMessage with an 'unmatched' address-pattern
is received, and no 'default' handler is registered.

#### Methods

---

### `NotSubscribedError(self, addr, prefix=None)`

This error is raised (by an OSCMultiClient) when an attempt is made to unsubscribe a host
that isn't subscribed.

#### Methods

---

### `OSCAddressSpace(self)`



#### Methods

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

---

### `OSCClient(self, server=None)`

Simple OSC Client. Handles the sending of OSC-Packets (OSCMessage or OSCBundle) via a UDP-socket
        

#### Methods

---

### `OSCClientError(self, message)`

Class for all OSCClient errors
        

#### Methods

---

### `OSCError(self, message)`

Base Class for all OSC-related errors
        

#### Methods

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

---

### `OSCMultiClient(self, server=None)`

'Multiple-Unicast' OSC Client. Handles the sending of OSC-Packets (OSCMessage or OSCBundle) via a UDP-socket
This client keeps a dict of 'OSCTargets'. and sends each OSCMessage to each OSCTarget
The OSCTargets are simply (host, port) tuples, and may be associated with an OSC-address prefix.
the OSCTarget's prefix gets prepended to each OSCMessage sent to that target.

#### Methods

---

### `OSCRequestHandler(self, request, client_address, server)`

RequestHandler class for the OSCServer
        

#### Methods

---

### `OSCServer(self, server_address, client=None, return_port=0)`

A Synchronous OSCServer
Serves one request at-a-time, until the OSCServer is closed.
The OSC address-pattern is matched against a set of OSC-adresses
that have been registered to the server with a callback-function.
If the adress-pattern of the message machtes the registered address of a callback,
that function is called. 

#### Methods

---

### `OSCServerError(self, message)`

Class for all OSCServer errors
        

#### Methods

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

---

### `OSCStreamingServer(self, address)`

A connection oriented (TCP/IP) OSC server.
        

#### Methods

---

### `OSCStreamingServerThreading(self, address)`

Mix-in class to handle each request in a new thread.

#### Methods

---

### `ThreadingOSCRequestHandler(self, request, client_address, server)`

Multi-threaded OSCRequestHandler;
Starts a new RequestHandler thread for each unbundled OSCMessage

#### Methods

---

### `ThreadingOSCServer(self, server_address, client=None, return_port=0)`

An Asynchronous OSCServer.
This server starts a new thread to handle each incoming request.

#### Methods

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

