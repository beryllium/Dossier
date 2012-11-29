Dossier
=======

Dynamic tool for managing EC2 security groups in a mid-size company (several groups spread over several amazon accounts)

Currently, only bin/get-all-groups.py is implemented. It takes an individual set of credentials on the command line, and returns either plaintext or CSV analysis of all EC2 security groups under those credentials. In theory, this spans all amazon regions, but I haven't specifically tested that yet.

My plan is to create a set of classes that I can tie together to achieve the goal stated above - automatable management of complex configurations (likely including security group configurations for non-EC2 AWS services). I'm relatively new to python, though, so guidance and assistance is more than welcome! :)
