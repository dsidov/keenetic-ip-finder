import requests
import argparse
import sys

parser = argparse.ArgumentParser(description='IP address finder for ZyXEL Keenetic router in Repeater/Extender mode.')
parser.add_argument('-a','--address', type=str, default='192.168.1.1', action='store', help='Custom IP adress instead of 192.168.1.x')
parser.add_argument('-l','--login', type=str, action='store', help='Admin login')
parser.add_argument('-p','--password', type=str, action='store', help='Admin password')
parser.add_argument('--fast', '-f', action='store_true', help='Stops the script after first matching address was found.')
args = parser.parse_args()

# address formatting
addr_l = args.address.split('.')
if len(addr_l) < 3:
	print('ERROR: Custom IP address error. Program terminated.')
	sys.exit()
addr_b = '.'.join(addr_l[:3]) + '.'

no_results = True
addr_dict = dict()

print('Searching for Keenetic Lite IP. It may take a while...')
for i in range(256):
	addr = addr_b + str(i)
	sys.stdout.write('\r' + 'Checking address ' + addr + ' / 255')
	addr_f = 'http://' + addr
	try:
		response = requests.get(addr_f)
	except OSError:
		pass
	else:
		if response.status_code not in addr_dict:
			addr_dict[response.status_code] = list()
			addr_dict[response.status_code].append(addr)
		else:
			addr_dict[response.status_code].append(addr)

		if response.status_code == 401: 
			if (args.login is not None) and (args.password is not None):
				try:
					response_f = requests.get(addr_f, auth=requests.auth.HTTPDigestAuth(args.login, args.password))
				except Exception:
					pass
				else:
					if response_f.status_code == 200:
						sys.stdout.flush()
						sys.stdout.write('\rMatching address found: ' + addr + '\r\n')
						no_results = False
						if args.fast:
							break
			else:	
				sys.stdout.flush()
				sys.stdout.write('\rPotential address found: ' + addr + '\r\n')
				no_results = False
				if args.fast:
					break
	sys.stdout.flush()
        
if no_results and len(addr_dict) > 0:
	print('\nDidn\'t found matching IP.')
	if 401 in addr_dict.keys():
		print('Possible address(es) without authorization:') 
		for addr in addr_dict[401]:
			print(addr)
		addr_dict.pop(401)
	if len(addr_dict) > 0:
		for key in addr_dict.keys():
			print(f'Address(es) with code {key}:')
			for addr in addr_dict[key]:
				print(addr)
else:
	print('No matching IPs found.')