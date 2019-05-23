from googleapiclient.discovery import build
import os
import string
import random
import re
import threading
import paramiko
from ..pluginbase import PluginBase

@PluginBase.register
class GoogleService():
	def __init__(self):
		self.type = "GOOGLE SERVICE"
		self.name = "Google"
		self.configured = True
		credentials = ''
		self.project_name = ''
		self.username = ''
		self.zone = 'us-east1-c'

		for file in os.listdir('plugins/GoogleService/googleCredentials/'):
			if file.endswith('.json'):
				credentials = (os.path.join('plugins/GoogleService/googleCredentials/', file))
		if(credentials == ''):
			print("No google credential file found")
			self.configured = False

		os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials

		try:
			self.compute = build('compute', 'v1')
		except Exception :
			print("Google compute has not been configured!")
			self.configured = False
		
		try:
			self.cloudresourcemanager = build('cloudresourcemanager', 'v1')
			request = self.cloudresourcemanager.projects().list()
			response = request.execute()
			for project in response.get('projects', []):
				self.project_name = project.get('projectId')
				break
		except Exception :
			print("Google compute has not been configured!")
			self.configured = False
		
		try:
			request = self.compute.projects().get(project=self.project_name)
			response = request.execute()
			metadata = response.get('commonInstanceMetadata')
			items = metadata.get('items')
			for item in items:
				if(item.get('key') == 'ssh-keys'):
					rsa = item.get('value')
					self.username = rsa.rsplit(' ', 1)[1]
		except Exception:
			print("Google compute has not been configured!")
			self.configured = False

		

	def check_setup(self):
		return self.configured

	def create_instance(self, group, size, num):
		print("Creating Instance...")
		# Get the latest Debian Jessie image.

		i = 1
		while i <= num:
			name = self.name.lower() + '-'
			name += ''.join(random.choice(string.ascii_lowercase) for _ in range(2))
			name += ''.join(random.choice(string.digits) for _ in range(2))
			image_response = self.compute.images().getFromFamily(
				project='debian-cloud', family='debian-9').execute()
			source_disk_image = image_response['selfLink']

			pattern = re.compile("[a-z]([-a-z0-9]*[a-z0-9])?")
			if not pattern.match(group):
				print("group name does not match regular expression")
				print(" first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.")
				print("try creating your instance again")
				return
			
			# Configure the machine
			machine_type = "zones/%s/machineTypes/%s" % (self.zone, size)
			config = {
				'name': name,
				'machineType': machine_type,
				'tags': {
					'items': [group]
				},

				# Specify the boot disk and the image to use as a source.
				'disks': [
					{
						'boot': True,
						'autoDelete': True,
						'initializeParams': {
							'sourceImage': source_disk_image,
						}
					}
				],

				# Specify a network interface with NAT to access the public
				# internet.
				'networkInterfaces': [{
					'network': 'global/networks/default',
					'accessConfigs': [
						{'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
					]
				}],

				# Allow the instance to access cloud storage and logging.
				'serviceAccounts': [{
					'email': 'default',
				'scopes': [
					'https://www.googleapis.com/auth/devstorage.read_write',
					'https://www.googleapis.com/auth/logging.write'
				]
				}],
			}
			self.compute.instances().insert(project=self.project_name, zone=self.zone, body=config).execute()
			print("Created Instance %d" % i)
			i = i + 1
		print("All instances created")
		print("Rerun %guppi cloud to display.")

	def get_instances_info(self):
		# Get instances from Google Compute
		instances = self.compute.instances().list(project=self.project_name, zone=self.zone).execute()
		instancesFormatted = []
		instances = instances.get('items', '')
		
		for instance in instances:
			machineType = instance.get('machineType', '').rsplit('/', 1)[-1]
			zone = instance.get('zone', '').rsplit('/', 1)[-1]
			state = instance.get('status', '')
			state = state.lower()
			if state == 'terminated':
				state = 'stopped'
			elif state == 'stopping':
				state = 'shutting-down'
			tags = instance.get('tags')
			items = tags.get('items')
			networkInterfaces = instance.get('networkInterfaces', [])
			accessConfigs = networkInterfaces[0].get('accessConfigs', [])
			externalIP = accessConfigs[0].get('natIP', '0')
			formatInst = {
				'Name': instance.get('name', ''),
				'Service': self.name,
				'Instance Id': instance.get('name', ''), # using name instead for now
				'Instance Type': machineType,
				'Availability Zone': zone,
				'State': state,
				'Key Name': '',
				'Launch Time': instance.get('creationTimestamp', ''),
				'Dns': externalIP,
				'External IP': externalIP,
				'Group Name': items[0]
			}
			
			instancesFormatted.append(formatInst)
				
		return instancesFormatted

	def terminate_instance(self,index):
		print("Terminating Instance...")
		instances = self.get_instances_info()
		name = instances[index]['Instance Id']
		self.compute.instances().delete(
				project=self.project_name,
				zone=self.zone,
				instance=name).execute()
		print("Google Instance Terminated.")
		print("Rerun %guppi cloud to update.")
	
	def toggle_instance(self,index):
		instances = self.get_instances_info()
		name = instances[index]['Instance Id']

		current_state = instances[index]['State']
		if(current_state == "running"):
			self.compute.instances().stop(
				project=self.project_name,
				zone=self.zone,
				instance=name).execute()
			print("Instance Stopped.")
			print("Rerun %guppi cloud to update.")

		elif(current_state == "stopped"):
			self.compute.instances().start(
				project=self.project_name,
				zone=self.zone,
				instance=name).execute()
			print("Instance Started.")
			print("Rerun %guppi cloud to update.")

	def reboot_instance(self,index):
		instances = self.get_instances_info()
		name = instances[index]['Instance Id']
		self.compute.instances().reset(
				project=self.project_name,
				zone=self.zone,
				instance=name).execute()
		print("Instance Rebooted.")
		print("Rerun %guppi cloud to update.")
	
	def ssh(self, instances, commands, verbose):
		# clear_output()
		# print("Running, please wait...")
		
		# threadOutputList contains list of all shell outputs
		threadOutputList = []
		
		# threadErrorList contains list of all shell errors
		threadErrorList = []
		
		# sshThread gets called by each thread
		def sshThread(commands, instanceId):
			# set the dns for each instance
			Dns = ''
			for vm in instances:
				if(instanceId == vm['Instance Id'] or instanceId == vm['Name']):
					Dns = vm['Dns']
			
			# ssh in and run commands
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			user_and_key = self.get_user_and_keyname()

			ssh.connect(Dns,
						username=user_and_key[0],
						key_filename=user_and_key[1])
		
			stdin, stdout, stderr = ssh.exec_command(commands)
			stdin.flush()
			
			# create list of all lines of output
			outputList = []
			outputList.append("=======================================================")
			outputList.append(instanceId)
			outputList.append("=======================================================")
			for line in stdout.read().splitlines():
				outputList.append(line)
			# create list of all lines of errors
			errorList = []
			errorList.append("=======================================================")
			errorList.append(instanceId)
			errorList.append("=======================================================")
			errorOutput = stderr.read().splitlines()
			numOfCommands = len(commands.split(" "))
			
			# if no errors append "successfully run" to output and error lists
			if len(errorOutput) == 0:
				if numOfCommands == 1:
					errorList.append("Successfully ran 1 command\n")
					outputList.append("Successfully ran 1 command\n")
				else:
					errorList.append("Successfully ran " + str(numOfCommands) + " commands\n")
					outputList.append("Successfully ran " + str(numOfCommands) + " commands\n")
			
			# append errors to the errorList
			for line in errorOutput:
				errorList.append(line)

			# append errorList to threadErrors
			threadErrorList.append(errorList)

			# append outputList to the threadOutputs
			threadOutputList.append(outputList)
			
			# disconnect from instance
			ssh.close()
		
		# theadList will contain a thread for each instance
		threadList = []
		
		# for each checked instance create a thread
		for instance in instances:
			thread = threading.Thread(target=sshThread, args=(commands, instance['Instance Id'])) 
			thread.start()
			threadList.append(thread)

		# wait for each thread to finish
		for thread in threadList:
			thread.join()
		
		# if verbose flag is used print output from each instance shell
		if verbose:		
			for data in threadOutputList:
				for output_line in data:
					print(output_line)
		# else just print errors from each instance shell
		else:
			for errors in threadErrorList:
				for output_line in errors:
					print(output_line)	
	

	def update_group(self, instance_id, group_name):

		request = self.compute.instances().get(project=self.project_name, zone=self.zone, instance=instance_id[0])
		instance = request.execute()
		tags = instance.get('tags')
		fingerprint = tags.get('fingerprint')
		tags_body = {
			"items": [group_name],
			"fingerprint": fingerprint 
		}
		self.compute.instances().setTags(project=self.project_name, zone=self.zone, instance=instance_id[0], body=tags_body).execute()

	
	def get_size_list(self):
		return ['n1-standard-1','n1-standard-2','n1-standard-4','n1-standard-8','n1-standard-16','n1-standard-32','n1-standard-64','n1-standard-96','n1-highmem-2','n1-highmem-4','n1-highmem-8','n1-highmem-16','n1-highmem-32','n1-highmem-64','n1-highmem-96','n1-highcpu-2','n1-highcpu-4','n1-highcpu-8','n1-highcpu-16','n1-highcpu-32','n1-highcpu-64','n1-highcpu-96','f1-micro','g1-small','n1-ultramem-40','n1-ultramem-80','n1-ultramem-160','n1-megamem-96']

	def get_default_size(self):
		return 'n1-standard-1'
	
	def get_user_and_keyname(self):
		return [self.username, './plugins/GoogleService/gc_rsa.pem']