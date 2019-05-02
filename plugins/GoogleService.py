from pluginbase import PluginBase
from googleapiclient.discovery import build
import os
import string
import random
import re

credentials = ''
for file in os.listdir('plugins/googleCredentials/'):
    if file.endswith('.json'):
        credentials = (os.path.join('plugins/googleCredentials/', file))
if(credentials == ''):
	print("No google credential file found")
else:
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials

	compute = build('compute', 'v1')
	cloudresourcemanager = build('cloudresourcemanager', 'v1')


	project_name = ''
	zone = 'us-east1-c'

	# The following code gets the project id
	# Todo: support selecting specific project
	# while True:

	request = cloudresourcemanager.projects().list()
	response = request.execute()

	for project in response.get('projects', []):

		project_name = project.get('projectId')
		break
		# break
	#     request = service.projects().list_next(previous_request=request, previous_response=response)

@PluginBase.register
class GoogleService():
	def __init__(self):
		self.type = "GOOGLE SERVICE"
		self.name = "Google"
	
	def check_setup(self):
		if credentials == '':
			return False
		return True

	def create_instance(self, group, size, num):
		print("Creating Instance...")
		# Get the latest Debian Jessie image.

		i = 1
		while i <= num:
			name = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
			name = name + ''.join(random.choice(string.digits) for _ in range(4))
			image_response = compute.images().getFromFamily(
				project='debian-cloud', family='debian-9').execute()
			source_disk_image = image_response['selfLink']

			pattern = re.compile("[a-z]([-a-z0-9]*[a-z0-9])?")
			if not pattern.match(group):
				print("group name does not match regular expression")
				print(" first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.")
				print("try creating your instance again")
				return
			
			# Configure the machine
			machine_type = "zones/%s/machineTypes/%s" % (zone, size)
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
			compute.instances().insert(project=project_name, zone=zone, body=config).execute()
			print("Created Instance %d" % i)
			i = i + 1
		print("All instances created")
		print("Rerun %guppi cloud to display.")

	def get_instances_info(self):
		global zone
		# Get instances from Google Compute
		instances = compute.instances().list(project=project_name, zone=zone).execute()
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
			formatInst = {
				'Name': instance.get('name', ''),
				'Instance Id': instance.get('name', ''), # using name instead for now
				'Instance Type': machineType,
				'Availability Zone': zone,
				'State': state,
				'Key Name': '',
				'Launch Time': instance.get('creationTimestamp', ''),
				'Dns': '',
				'Group Name': items[0]
			}
			
			instancesFormatted.append(formatInst)
				
		return instancesFormatted

	def terminate_instance(self,index):
		print("Terminating Instance...")
		instances = self.get_instances_info()
		name = instances[index]['Instance Id']
		compute.instances().delete(
				project=project_name,
				zone=zone,
				instance=name).execute()
		print("Google Instance Terminated.")
		print("Rerun %guppi cloud to update.")
	
	def toggle_instance(self,index):
		instances = self.get_instances_info()
		name = instances[index]['Instance Id']

		current_state = instances[index]['State']
		if(current_state == "running"):
			compute.instances().stop(
				project=project_name,
				zone=zone,
				instance=name).execute()
			print("Instance Stopped.")
			print("Rerun %guppi cloud to update.")

		elif(current_state == "stopped"):
			compute.instances().start(
				project=project_name,
				zone=zone,
				instance=name).execute()
			print("Instance Started.")
			print("Rerun %guppi cloud to update.")

	def reboot_instance(self,index):
		instances = self.get_instances_info()
		name = instances[index]['Instance Id']
		compute.instances().reset(
				project=project_name,
				zone=zone,
				instance=name).execute()
		print("Instance Rebooted.")
		print("Rerun %guppi cloud to update.")
