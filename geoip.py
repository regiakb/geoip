#!/usr/bin/env python

import requests
import sys
import csv
import string
import re
import os,sys
import pandas as pd
from lxml import html
from bs4 import BeautifulSoup
import regex

if len(sys.argv) < 2:
    sys.stderr.write('How to use = python3 geoip.py IP.csv\n')
    exit(1)

# open csv object
with open(sys.argv[1]) as file:
  # read values of each row({header : value})
  reader = csv.DictReader(file)
  data = {}
  for row in reader:
    for header, value in row.items():
      try:
        data[header].append(value)
      except KeyError:
        data[header] = [value]

# ips = name of column of csv
ip = data['IP Address']

def get_ip_country(ip):
    response = requests.get('http://ip2c.org/{}'.format(ip))
    error_codes = [ 'WRONG INPUT', 'UNKNOWN' ] # http://about.ip2c.org/#outputs

    country_name = response.text.split(';')[3]

    if response.status_code != 200 or country_name in error_codes:
        sys.stderr.write('No information of IP {} - Skipping.\n'.format(ip))
        return False

    if country_name == 'Reserved':
        sys.stderr.write('It is not possible to retrieve information from a private IP {} \n'.format(ip))
        return False

    country_code = response.text.split(';')[1]

    return {
        'country_name': country_name, 
        'country_code': country_code
    }

ip_list = list(ip)

#results
for ip in ip_list:
    result = get_ip_country(ip)
    if result:
        print(ip, ";", result['country_name'], "\n")

