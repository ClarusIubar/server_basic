import socket 

host_name = "localhost"
addr = socket.getaddrinfo(host_name, None)

for res in addr:
    print(f"family: {res[0].name}, address: {res[4][0]}")
    # family: AF_INET6, address: ::1
    # family: AF_INET, address: 127.0.0.1
