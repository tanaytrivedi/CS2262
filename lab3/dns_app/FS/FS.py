from flask import Flask, request, jsonify
from flask import Response
import socket
import json

app = Flask(__name__)

HOST = '172.17.0.2'
AUTH_SERVER_PORT = 53533


@app.route('/register', methods = ['POST'])
def register():
	data = request.json
	auth_request = {'TYPE': 'A','NAME': data['hostname'],'VALUE': data['ip'],'TTL': 10} 
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, AUTH_SERVER_PORT))
		s.sendall((json.dumps(auth_request)).encode())
		data = s.recv(1024)

	j = json.loads(data.decode())
	if j['registration'] == 'SUCCESS':
		status_code =  Response(status=201)
		return status_code

@app.route('/fibonacci', methods = ['GET'])
def fibonacci():
	X = request.args.get('number')
	try:
		X = int(X)
		print('Got Fib Request for X=' + str(X))
		fib_return = run_fib_request(X)
		print('Fib Value = ' + str(fib_return))
		return jsonify({'fib': fib_return})
	except ValueError:
		return Response(status = 400)

def run_fib_request(number):
	if number == 1:
		return 0
	if number == 2:
		return 1
	return run_fib_request(number - 1) + run_fib_request(number - 2)


app.run(host='0.0.0.0',
        port=9090,
        debug=True)
