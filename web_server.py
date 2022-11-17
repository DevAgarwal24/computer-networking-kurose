from socket import *
import sys # In order to terminate the program

import datetime
import pytz

host = 'localhost'
port = 2407

day = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 7: 'Sun'}
month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

status_code = {200: 'OK', 404: 'File not found'}

#####################################################
def get_date_and_time():
    ct = datetime.datetime.now(pytz.timezone('GMT'))
    date = f"Date: {day[ct.weekday()]}, {ct.day} {month[ct.month]} {str(ct.year)} {str(ct.hour).zfill(2)}:{str(ct.minute).zfill(2)}:{str(ct.second).zfill(2)} GMT"
    return date


def parse_http_request(http_request):
    request = http_request.pop(0)
    request = request.split()

    headers = dict()
    for header in http_request:
        if header == '':
            continue
        header = header.split(': ')
        headers[header[0]] = header[1]

    return request, headers


def create_http_response(data):
    response = f"""
Server: SimpleHTTP
{get_date_and_time()}
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: {len(data)}

{data}"""

    return response

#####################################################

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind((host, port))
serverSocket.listen(1)

while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        print('\n\nNew Connetion')

        message = connectionSocket.recv(2048)
        if message == b'':
            connectionSocket.close()
            continue

        http_request = message.decode().splitlines()
        request, headers = parse_http_request(http_request)

        filename = request[1]

        f = open(filename[1:])
        output_data = f.read()
        f.close()
        response = create_http_response(output_data)

        connectionSocket.send(f"HTTP/1.0 200 {status_code[200]}".encode())
        connectionSocket.send(response.encode())
        connectionSocket.send("\r\n".encode())
    except IOError:
        f = open('not_found.html')
        output_data = f.read()
        f.close()
        response = create_http_response(output_data)

        connectionSocket.send(f"HTTP/1.0 404 {status_code[404]}".encode())
        connectionSocket.send(response.encode())
        connectionSocket.send("\r\n".encode())

    connectionSocket.close()

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data
