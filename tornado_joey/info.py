import os.path
import boto3   
def main():
	ec2client = boto3.client('ec2')
	response = ec2client.describe_instances()
	print(response)