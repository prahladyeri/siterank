#!/usr/bin/env python3
##
# Script to fetch alexa ranks for one or more websites.
# Usage: siterank <url1> <url2> ....
#
# @author Prahlad Yeri
#
import urllib.request
import sys, os
import argparse
import xml.etree.ElementTree as ET
from siterank import __title__, __version__

def main():
	# if len(sys.argv) == 1:
		# print("Insufficient parameters.")
		# exit()
	# urls = sys.argv[1:]
	if '-v' in sys.argv or '--version' in sys.argv:
		print( "%s version %s" % (__title__, __version__) )
		return
	parser = argparse.ArgumentParser()
	parser.add_argument('list', nargs='+', default=[], help='List of URLs EX: www.google.com www.yahoo.com etc.')
	parser.add_argument('-v', '--version', help='Display Version', action='store_true')
	args = parser.parse_args()
	
	
	ranks = {}
	for url in args.list:
		#https://stackoverflow.com/questions/3676376/fetching-alexa-data
		turl = "http://data.alexa.com/data?cli=10&url=" + url
		req = urllib.request.Request(turl)
		with urllib.request.urlopen(req) as fp:
			output = fp.read().decode('utf-8')
			tree = ET.ElementTree(ET.fromstring(output))
			root = tree.getroot()
			sd = root.find("SD")
			if sd != None:
				rnk = int(sd.find("POPULARITY").get("TEXT"))
				ranks[url] = rnk
			else:
				print("Not found: " + url)
	sranks = [(k,ranks[k] if ranks[k]<1000 else str(int(ranks[k]/1000)) + "k") for k in sorted(ranks, key=ranks.get, reverse=False)]
	
	col_len = 40
	cols = 2
	#row_format ="{:>10}" * (len(sranks.keys()) + 1)
	row_format = ("{:<%d}" % col_len) * cols
	print("")
	print("*" * col_len * cols)
	print(" ", row_format.format("Website", "Rank"))
	print("*" * col_len * cols)
	for k,v in sranks:
		# rank = v
		# if rank > 1000:
			# rank = str(int(rank/1000)) + "K"
		#print(k, v)
		print(" ", row_format.format(k, v))

if __name__ == "__main__":
	main()
