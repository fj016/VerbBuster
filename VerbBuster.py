import requests as rq
import concurrent.futures
import os
import time
import argparse
import signal
import sys

good_url = 0
maybe_url = 0
bad_url = 0
wrong_trace = 0
good_trace = 0

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'}

def sigint_handler(signal, frame):
    print ('KeyboardInterrupt is caught')
    os._exit(1)
    
def result_print(ok, maybe, error):
	os.system("clear")
	print("Good URLs found (2XX) : " + str(ok))
	print("Maybe OK URLs found (3XX-403): " + str(maybe))
	print("Bad URLs found (4XX-5XX): " + str(error))
	
	
def result_print_trace(ok, error, method):
	os.system("clear")
	print("URLs accepting " + str(method) + " found (2XX) : " + str(ok))
	print("Bad URLs not accepting TRACE found (4XX-5XX): " + str(error))
	
	
def trace(url_trace, filename, custom):
	global wrong_trace
	global good_trace
	try:
		trace_req = rq.request(custom, url_trace, headers=headers)
		sc_trace = trace_req.status_code
		
		if sc_trace in range(200,405):
			good_trace += 1
			ok_trace = open(str(filename)+ '_trace_ok.txt', 'a')
			ok_trace.write(f"{url_trace}\n")
			ok_trace.close()
		else:
			wrong_trace += 1
			
	except requests.ConnectionError:
			print("Failed to connect\n")
			print("Host may be down or blocking our req.\n")
			
	return good_trace, wrong_trace, custom
	
		
def get_status(url, filename):
	global good_url
	global maybe_url
	global bad_url
	
	try:
		fast_req = rq.head(url, headers=headers)
		sc = fast_req.status_code
		
		if sc in range(200, 300):
			good_url += 1
			ok_file = open(str(filename) +'_OK.txt', 'a')
			ok_file.write(f"{url}\n")
			ok_file.close()
		elif sc in range(300, 404):
			maybe_url += 1
			maybe_file = open(str(filename) + '_maybe.txt', 'a')
			maybe_file.write(f"{url}\n")
			maybe_file.close()
		else:
			bad_url += 1
	
	except requests.ConnectionError:
			print("Failed to connect\n")
			print("Host may be down or blocking our req.\n")
			
	return good_url, maybe_url, bad_url
			

parser = argparse.ArgumentParser(description="Validate a list of URLs or discover endpoints that uses exotic HTTP verbs.")
parser.add_argument("-l", "--list", type=str, help="File containing a list of URLS to scan", required=True)
parser.add_argument("-m", "--mode", type=str, help="The mode you want to use", required=True, choices=['validate', 'trace', 'custom'])
parser.add_argument("-c", "--custom", type=str, help="The custom verb to use if mode set to custom")
parser.add_argument("-oN", "--output-name", type=str, help="The path and prefix to output files", required=True)


args = parser.parse_args()
verb = 'TRACE'

signal.signal(signal.SIGINT, sigint_handler)
if args.mode == 'custom':
	if args.custom is None:
		parser.error('You need to supply a custom verb with the custom mode')
	else:
		verb = args.custom
		
my_result = args.output_name
my_target = args.list

if args.mode == 'validate':
	with open(my_target, 'r') as target:
		with concurrent.futures.ThreadPoolExecutor() as executor:
			futures = []
			print("Loading pool...")
			time.sleep(1)
			for line in target:
				line_good = line.strip()
				futures.append(executor.submit(get_status, line_good, my_result))
			print("Lauching scan...")
			time.sleep(1)
			os.system("clear")
			for future in concurrent.futures.as_completed(futures):
				result_print(*future.result())
else:				
	with open(my_target, 'r') as target:
		with concurrent.futures.ThreadPoolExecutor() as executor:
			futures = []
			print("Loading pool... (This may take some time depending on the size of the list")
			time.sleep(1)
			for line in target:
				line_good = line.strip()
				futures.append(executor.submit(trace, line_good, my_result, verb))
				
			for future in concurrent.futures.as_completed(futures):
				result_print_trace(*future.result())
				
