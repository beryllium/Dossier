Dossier
=======

Dynamic tool for managing EC2 security groups in a mid-size company (several groups spread over several amazon accounts)

Currently, only bin/get-all-groups.py is implemented. It can be configured system- or user-wide, or take an individual set of credentials on the command line. It returns either plaintext or CSV analysis of all EC2 security groups under the supplied credentials. In theory, this spans all amazon regions, but I haven't specifically tested that yet.

My plan is to create a set of classes that I can tie together to achieve the goal stated above - automatable management of complex configurations (likely including security group configurations for non-EC2 AWS services). I'm relatively new to python, though, so guidance and assistance is more than welcome! :)

Configuration
-------------

The latest update lets you create an account configuration file in either /etc/dossier.ini or ~/.dossier.ini, containing a number of accounts. 

It should follow a structure like so:

    [accountname1]
    access:
    secret:

    [mysecondaccount]
    access:
    secret:

When initiated, if the user does not specify a key/secret on the command line, the get-all-groups script will iterate through all EC2 regions and check all the security groups for each account. Horribly inefficient, but it seems to work for now. Specifying a key/secret on the command line resets the account list to a single account named "custom-cli", bypassing this configuration file.

Usage
-----

To list all security groups of all accounts in your dossier.ini:

    bin/get-all-groups.py

To scan security groups of a single account:

    bin/get-all-groups --key "mykey" --secret "mysecret"

To output in CSV format:

    bin/get-all-groups --csv

Future Plans
------------

I plan to integrate an ORM or similar solution (perhaps Storm) so that the tool can constantly monitor security group changes. I also want to enable the ability to name individual rules, and possibly set expiry times on them, so the tool can grow to be more useful in a production environment. 
