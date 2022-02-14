from flask import Flask, request, Response, jsonify
import requests
import json
import socket

app = Flask(__name__)

FIBONACCI_KEYS = set(['hostname', 'fs_port', 'number', 'as_ip', 'as_port'])

@app.route('/fibonacci', methods = ['GET'])
def fibonacci():
	req_dict = dict(request.args)
	req_keys = set(req_dict.keys())

	if req_keys == FIBONACCI_KEYS:
		print('US Received Request')
		print(request.args)
		hostname = request.args.get('hostname')
		fs_port = request.args.get('fs_port')
		number = request.args.get('number')
		as_ip = request.args.get('as_ip')
		as_port = request.args.get('as_port')

		ip_request = {'TYPE': 'A','NAME': hostname}
		print('Sending Socket Request')
		print(ip_request)


		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((as_ip, int(as_port)))
			s.sendall((json.dumps(ip_request)).encode())
			data = s.recv(1024)
		data = json.loads(data.decode())
		print(type(data))
		print(data)
		ip_address = data['VALUE']
		html='http://{}:{}/fibonacci?number={}'.format(ip_address,fs_port,number)
		print('Fibonacci url = ' + html)
		r = requests.get(html)
		print(r.content)
		return jsonify(r.json())

	else:
		return Response(status = 400)



app.run(host='0.0.0.0', port=8080, debug=True)
