#!/usr/bin/env python3

import os
import sys
import json
import argparse
import datetime
import requests


parser = argparse.ArgumentParser(
    description="Shows tracked time with Freshdesk")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-y", "--yesterday", action="store_true",
                   help="shows time, tracked yesterday")
group.add_argument("-t", "--today", action="store_true",
                   help="shows time, tracked today")
group.add_argument("-d", "--date", type=str,
                   help="shows time, tracked during specific date with format DD-MM-YYYY, for example 17-10-2022")
parser.add_argument("-k", "--key", type=str,
                    help="Freshdesk API key, this option has higher priority than FRESHDESK_API_KEY environment varible")
parser.add_argument("-f", "--fdomain", type=str,
                    help="Your Freshdesk domain (your should not enter \'freshdesk.com\' here). This option has higher priority than FRESHDESK_DOMAIN environment varible")
args = parser.parse_args()

if args.date:
  initial_date_time = datetime.datetime.strptime(args.date, "%d-%m-%Y").strftime('%Y-%m-%dT00:00:00Z')
  end_date_time = (datetime.datetime.strptime(args.date, "%d-%m-%Y") +
                   datetime.timedelta(hours=23,minutes=59,seconds=59)).strftime('%Y-%m-%dT%H:%M:%SZ')
elif args.today:
  initial_date_time = datetime.date.today().strftime('%Y-%m-%dT00:00:00Z')
  end_date_time = datetime.datetime.today().replace(
      hour=23, minute=59, second=59).strftime('%Y-%m-%dT%H:%M:%SZ')
elif args.yesterday:
  initial_date_time = (datetime.date.today()-datetime.timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z')
  yesterday = datetime.date.today() - datetime.timedelta(days=1)
  t = datetime.time(hour=23, minute=59, second=59)
  end_date_time = datetime.datetime.combine(yesterday, t).strftime('%Y-%m-%dT%H:%M:%SZ')

if args.key:
  api_key = args.key
elif os.environ.get('FRESHDESK_API_KEY'):
  api_key = os.environ.get('FRESHDESK_API_KEY')
else:
  print("Freshdesk API key not found, please use \'-k\' option or FRESHDESK_API_KEY environment variable")
  sys.exit(1)

if args.fdomain:
  domain = args.fdomain
elif os.environ.get('FRESHDESK_DOMAIN'):
  domain = os.environ.get('FRESHDESK_DOMAIN')
else:
  print("Freshdesk domain is undefined, please use \'-f\' option or FRESHDESK_DOMAIN environment variable")
  sys.exit(1)

fd_domain = "https://" + domain + ".freshdesk.com/api/v2"
status_endpoint = fd_domain + '/agents/me'
headers = {"Content-Type": "application/json"}

responce = requests.get(status_endpoint, auth=(api_key, 'X'), headers=headers)
id=responce.json()["id"]

tickets_endpoint = fd_domain + "/time_entries"
params = dict(
    agent_id=id,
    executed_after=initial_date_time,
    executed_before=end_date_time,
)

responce = requests.get(tickets_endpoint, auth=(api_key, 'X'), headers=headers, params=params)

sum_time = datetime.timedelta()


for entry in responce.json():
  spec_ticket_endpoint = fd_domain + "/tickets/" + str(entry["ticket_id"])
  responce = requests.get(spec_ticket_endpoint, auth=(api_key, 'X'), headers=headers)
  print(responce.json()["subject"])
  print("Time tracked: " + entry["time_spent"])
  print("------------------------------------------------------------------")
  (h, m) = entry["time_spent"].split(":")
  tmp_time = datetime.timedelta(hours=int(h), minutes=int(m))
  sum_time += tmp_time

print ("Total time: " + str(sum_time))