#!/usr/bin/env python

import boto
import argparse
import ConfigParser
import os
from boto.ec2.connection import EC2Connection

def main():
  accounts = {}
  config = ConfigParser.ConfigParser()

  p = argparse.ArgumentParser(description="Fetch security groups from an amazon account.")
  p.add_argument('--key', '-k', help="Amazon AWS Access Key")
  p.add_argument('--secret', '-s', help="Amazon AWS Secret Key")
  p.add_argument('--csv', help="CSV output", action='store_true')
  arguments = p.parse_args()

  config.read(['/etc/dossier.ini', os.path.expanduser('~/.dossier.ini')])

  for section in config.sections():
    accounts[section] = { 'access':config.get(section,'access'), 'secret':config.get(section,'secret') }

  if ( arguments.key and arguments.secret ):
    accounts = { 'custom-cli': { 'access': arguments.key, 'secret': arguments.secret } }

  if len(accounts)==0:
    print "No accounts found. Please specify an account on the command line, or add accounts to a configuration file."
    return

  if arguments.csv is True:
    display_csv_header()

  for account_name, account in accounts.iteritems():
    rs = get_all_groups( account_name, account[ 'access' ], account['secret'] )
    if len(rs)>0:
      display_group( rs, account_name, arguments.csv )


def get_all_groups( account_name, access_key, secret_key ):
  try:
    conn = EC2Connection( access_key, secret_key )
    rs = conn.get_all_security_groups()
  except conn.ResponseError:
    print 'Access key rejected on account', account_name
    rs = []

  return rs

def display_group( rs, account_name = None, csv=False ):
  for group in rs:
    if csv is not True:
      print "%s: %s" % ( account_name, group.name )
    for element in group.rules:
      for ip in element.grants:
        if csv is True:
          print "%s,%s,%s,%s,%s,%s,%s" % ( account_name, group.name, element.from_port, element.to_port, ip.cidr_ip, ip.name, ip.owner_id )
        elif element.from_port == element.to_port:
          print "\tPort: %s\tIP/CIDR: %s" % ( element.from_port, ip )
        else:
          print "\tPort: %s-%s\tIP/CIDR: %s" % ( element.from_port, element.to_port, ip )

def display_csv_header():
  print 'account_name,group_name,from_port,to_port,grant_cidr_ip,grant_name,grant_owner'

if __name__ == '__main__':
  main()
