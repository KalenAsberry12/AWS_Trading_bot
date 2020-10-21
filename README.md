# AWS_Trading_bot

Team Members:
- Ivan Tatum
- Kalen Asberry
- Connor Gross
- Jonathan Park

The project seeks to deploy a simple trading bot using AWS / EC2 cloud services and Alpaca.markets platform. The main focus of the project is creating a successful integration between AWS EC2 and our python code to being traded on Alpaca, not on the success of the algorithm itself.

# Running Python scripts on an AWS EC2 Instance
https://medium.com/@praneeth.jm/running-python-scripts-on-an-aws-ec2-instance-8c01f9ee7b2f

## Step-by-Step to Build a Stock Trading Bot
https://alpaca.markets/learn/stock-trading-bot-instruction/

## Python client for Alpaca's trade API
https://pypi.org/project/alpaca-trade-api/


## Paper Trading Specification - Documentation | Alpaca
https://alpaca.markets/docs/trading-on-alpaca/paper-trading/


## Build a Day-Trading Algorithm and Run it in the Cloud — For Free
https://medium.com/automation-generation/build-a-day-trading-algorithm-and-run-it-in-the-cloud-for-free-805450150668



## Setting up an Amazon EC2 server to run an arbitrage trading bot for crypto exchanges
https://medium.com/@aymeric_nc/setting-up-an-amazon-ec2-server-to-run-an-arbitrage-trading-bot-for-crypto-exchanges-cafc8df8d2e0



## 10 visualizations to try in Amazon QuickSight with sample data
https://aws.amazon.com/blogs/big-data/10-visualizations-to-try-in-amazon-quicksight-with-sample-data/


## Step-by-step guide to running a simple trading algorithm in the cloud using Python, Alpaca, and AWS
https://medium.com/automation-generation/step-by-step-guide-to-run-a-simple-trading-algorithm-in-the-cloud-using-python-alpaca-and-aws-34c899b678b0


## Alpaca & Backtrader: Tools of the Trade (Part 1)
https://alpaca.markets/learn/backtrader-01/



## How to Connect to AWS EC2 instance with Git Bash CLI on windows 
https://www.youtube.com/watch?v=tPiLRXvkFeQ

## Step-by-step guide to run a simple trading algorithm in the cloud using Python, Alpaca, and AWS
https://medium.com/automation-generation/step-by-step-guide-to-run-a-simple-trading-algorithm-in-the-cloud-using-python-alpaca-and-aws-34c899b678b0


## Running Python scripts on an AWS EC2 Instance
https://medium.com/@praneeth.jm/running-python-scripts-on-an-aws-ec2-instance-8c01f9ee7b2f


## Step-by-step guide
·  Create an EC2 Instance
·  Create a new key pair (xxx.pem), save it
·  Gitbash (Connect to EC2 Instance):        
o  chmod 400 project3.pem 
o  ssh -i "project3.pem" ec2-user@ec2-3-134-105-246.us-east-2.compute.amazonaws.com
·  Gitbash (Transfer .env and algorithm to EC2 Instance)
o  scp -i project3.pem smaenv.py ec2-user@ec2-3-134-105-246.us-east-2.compute.amazonaws.com:~/  
o  scp -i project3.pem .env ec2-user@ec2-3-134-105-246.us-east-2.compute.amazonaws.com:~/
·  Gitbash (Install packages):
o  sudo yum install python36
o  sudo alternatives --set python /usr/bin/python3.6
o  python --version
o  cd /tmp
o  curl -O https://bootstrap.pypa.io/get-pip.py
o  sudo pip install --upgrade pip
o  pip3 --version
o  pip3 install selenium --user
o  sudo pip install -U python-dotenv
o  pip install matplotlib
o  pip3 install alpaca-backtrader-api
o  pip3 install datetime

.  python3 smaenv.py


## Thing you can use

https://aws.amazon.com/ecs/ 

https://aws.amazon.com/cloudformation/ 

https://www.serverless.com/

## https://aws.amazon.com/secrets-manager/
AWS Secrets Manager | Rotate, Manage, Retrieve Secrets | Amazon Web Services (AWS)
