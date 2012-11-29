#!/usr/bin/env python

import boto
import argparse
from boto.ec2.connection import EC2Connection

def main():
  p = argparse.ArgumentParser(description="Fetch security groups from an amazon account.")
  p.add_argument('--key', '-k', help="Amazon AWS Access Key")
  p.add_argument('--secret', '-s', help="Amazon AWS Secret Key")
  p.add_argument('--csv', help="CSV output", action='store_true')
  arguments = p.parse_args()

  if not ( arguments.key and arguments.secret ):
    p.error( "Both --key AND --secret must be set" )

  conn = EC2Connection( arguments.key, arguments.secret )
  rs = conn.get_all_security_groups()
  if arguments.csv is True:
      print 'group_name,from_port,to_port,grant_cidr_ip,grant_name,grant_owner'
  for group in rs:
    if arguments.csv is not True:
      print group.name
    for element in group.rules:
      for ip in element.grants:
        if arguments.csv is True:
          print "%s,%s,%s,%s,%s,%s" % ( group.name, element.from_port, element.to_port, ip.cidr_ip, ip.name, ip.owner_id )
        elif element.from_port == element.to_port:
          print "\tPort: %s\tIP/CIDR: %s" % ( element.from_port, ip )
        else:
          print "\tPort: %s-%s\tIP/CIDR: %s" % ( element.from_port, element.to_port, ip )

if __name__ == '__main__':
  main()
