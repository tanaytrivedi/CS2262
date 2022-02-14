import socket
from os.path import exists
import os
import pandas as pd
import json

print(os.getcwd())
DATA_FILE = 'registrations.csv'
write_status = False

"""if exists(DATA_FILE):
	df = pd.read_csv(DATA_FILE)
else:"""
	

def process_registration(data, df):
	first_len = df.shape[0]
	new_df = pd.Series(data)
	df = df.append(new_df, ignore_index = True)
	df = df.drop_duplicates()
	if df.shape[0] != first_len:
		return {'registration': 'SUCCESS'}, True, df
	else:
		return {'registration': 'SUCCESS'}, False, df

def process_query(data):
	return df[df.NAME == data['NAME']].iloc[-1].to_dict()


print('Receiving connections now')
df = pd.DataFrame()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('0.0.0.0', 53533))
    s.listen()
    while True:
	    conn, addr = s.accept()
	    with conn:
	        print('Connected by', addr)
	        while True:
	        	recv_message = conn.recv(1024)
	        	if not recv_message:
	        		break
	        	else:
	        		recv_message_data = json.loads(recv_message.decode())
	        		if 'VALUE' in recv_message_data:
	        			print('Received Registration')
	        			message, write_status, df = process_registration(recv_message_data, df)
	        			if write_status:
	        				df.to_csv(DATA_FILE, index = None)
	        				write_status = False
	        		else:
	        			print('Received Query')
	        			message = process_query(recv_message_data)
	        		conn.sendall((json.dumps(message)).encode())

"""


while True:
	recv_message, client_address = auth_socket.recvfrom(2048)
	recv_message_data = json.loads(recv_message.decode())
	if 'VALUE' in recv_message_data:
		print('Received Registration')
		message, write_status = process_registration(recv_message_data)
	else:
		print('Received Query')
		message = process_query(recv_message_data)

	auth_socket.sendto((json.dumps(message)).encode(), client_address)

	if write_status:
		df.to_csv(DATA_FILE, index = None)
		write_status = False

"""