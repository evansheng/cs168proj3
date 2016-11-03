import numpy as np
import subprocess
import json
import time
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plot
from matplotlib.backends import backend_pdf

def run_traceroute(hostnames, num_packets, output_filename):
	route = {}
	route["timestamp"] = time.time()
	for hostname in hostnames:
		ls_output = subprocess.check_output("traceroute -a -q " + str(num_packets) + " " + hostname, shell=True)
		route[hostname] = ls_output

	with open(output_filename, 'w') as outfile:
		json.dump(route, outfile)


def parse_traceroute(raw_traceroute_filename, output_filename):
	with open(raw_traceroute_filename) as data_file:
		data = json.load(data_file)
	for k,v in data.iteritems():
		if k != "timestamp":
			v = parse_helper(v)
			data[k] = v
	with open(output_filename, 'a') as outfile:
		json.dump(data, outfile)



def parse_helper(values):
	values = values.split("\n")
	retList = []
	currList = []
	for router in values:
		linesplit = [str(x) for x in router.split()]
		if not linesplit:
			break
		if "[" not in linesplit[0]:
			if linesplit[0] == "*":
				currList.append({"ip":"None", "name":"None", "asn":"None"})
				continue
			if currList:
				retList.append(currList)
			if linesplit[1] == "*" and linesplit[2] == "*":
				currList.append({"ip":"None", "name":"None", "asn":"None"})
				continue
			currList = []
			routerDict = {}
			offset = 0
			if linesplit[1] == "*":
				offset = 1
			routerDict["ip"] = linesplit[3+offset][1:len(linesplit[3+offset])-1]
			routerDict["name"] = linesplit[2+offset]
			routerDict["asn"] = linesplit[1+offset][3:len(linesplit[1+offset])-1]
			currList.append(routerDict)
		else:
			routerDict = {}
			routerDict["ip"] = linesplit[2][1:len(linesplit[2])-1]
			routerDict["name"] = linesplit[1]
			routerDict["asn"] = linesplit[0][3:len(linesplit[0])-1]
			currList.append(routerDict) 
	retList.append(currList)
	return retList

def parse_public_server_traceroute(raw_traceroute_filename, output_filename):
	with open(raw_traceroute_filename) as data_file:
		data = json.load(data_file)
	for k,v in data.iteritems():
		if k != "timestamp":
			v = public_parse_helper(v)
			data[k] = v
	with open(output_filename, 'a') as outfile:
		json.dump(data,outfile)	

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def public_parse_helper(values):
	values = values.split("\n")
	retList = []
	currList = []
	for router in values:
		linesplit = [str(x) for x in router.split()]
		print linesplit
		if not linesplit:
			break
		if len(linesplit) < 4:
			if is_number(linesplit[0]):
				if currList:
					retList.append(currList)
				currList = []
				routerDict = {}
				routerDict["ip"] = linesplit[1]
			else:
				routerDict = {}
				routerDict["ip"] = linesplit[0]
			routerDict["name"] = "None"
			routerDict["asn"] = "None"
			currList.append(routerDict)
			continue


		if "[" not in linesplit[3]:
			if linesplit[0] == "*":
				currList.append({"ip":"None", "name":"None", "asn":"None"})
				continue
			if currList:
				retList.append(currList)
			if linesplit[1] == "*" and linesplit[2] == "*":
				currList.append({"ip":"None", "name":"None", "asn":"None"})
				continue
			currList = []
			routerDict = {}
		
			routerDict["ip"] = linesplit[2][1:len(linesplit[2])-1]
			routerDict["name"] = linesplit[1]
			if len(linesplit) > 5:
				routerDict["asn"] = linesplit[4][:len(linesplit[4])-1]
			else:
				routerDict["asn"] = "None"
			currList.append(routerDict)
		else:
			routerDict = {}
			routerDict["ip"] = linesplit[2][1:len(linesplit[2])-1]
			routerDict["name"] = linesplit[1]
			routerDict["asn"] = linesplit[0][3:len(linesplit[0])-1]
			currList.append(routerDict) 
	retList.append(currList)
	return retList

    
if __name__ == "__main__":
	#experiment a
	#run_traceroute(["google.com", "facebook.com", "www.berkeley.edu", "allspice.lcs.mit.edu", "todayhumor.co.kr", "www.city.kobe.lg.jp", "www.vutbr.cz", "zanvarsity.ac.tz"],5,"experiment_a_out")
	#parse_traceroute("experiment_a_out", "tr_a.json")
	#experiment b
	#run_traceroute(["tpr-route-server.saix.net", "route-server.ip-plus.net", "route-views.oregon-ix.net", "route-server.eastern.allstream.com"], 2, "experiment_b_out")
	#parse_traceroute("experiment_b_out", "tr_b.json")
	
	#run_traceroute(["tpr-route-server.saix.net", "route-server.ip-plus.net", "route-views.oregon-ix.net", "route-server.eastern.allstream.com"], 2, "experiment_b_campus_out")
	parse_public_server_traceroute("experiment_b_route_servers_out", "public_test_out")
