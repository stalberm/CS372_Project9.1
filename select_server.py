# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def handle_listener(ready_socket, read_set):
    new_conn = ready_socket.accept()[0]
    print(f"{new_conn.getpeername()}: connected")
    read_set.add(new_conn)

def handle_standard(ready_socket, read_set):
    request = ready_socket.recv(4096)
    print(f"{ready_socket.getpeername()} {len(request)} bytes: {request}")
    if (len(request) == 0):
        read_set.remove(ready_socket)
        print(f"{ready_socket.getpeername()}: disconnected")

def run_server(port):

    listener = socket.socket()
    listener.bind(('', int(port)))
    listener.listen()
    read_set = {listener}

    while True:

        read, _, _ = select.select(read_set, {}, {})

        for ready_socket in read:
            if ready_socket == listener:
                handle_listener(ready_socket, read_set)
            else:
                handle_standard(ready_socket, read_set)


#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
