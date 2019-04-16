from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute.models import DiskCreateOption
from pluginbase import PluginBase
import random
import re

class LocalBaseClass:
	pass
@PluginBase.register
class MicrosoftService(LocalBaseClass):
	def __init__(self):
		self.type = "AZURE SERVICE"
		# credentials
		self.client_id = '1858e2f8-7a54-4898-be37-b922a72b737f'
		self.secret = 'jAzDkyVPFNfjF7QBPsgUr9/BynIhUQMeFCStbd3GE2A='
		self.tenant = 'ad7ce373-aa8e-43d4-adab-480653dff4df'
		self.SUBSCRIPTION_ID = '96c2b8eb-ed80-462e-901f-4047a240bae1'
		self.GROUP_NAME = 'guppi'
		self.LOCATION = 'westus'
		self.credentials = ServicePrincipalCredentials(
			client_id = self.client_id,
			secret = self.secret,
			tenant = self.tenant
		)
		self.USERNAME = 'project.guppi@gmail.com'
		self.PASSWORD = 'GuppiCisco116'
		# clients
		self.resource_group_client = ResourceManagementClient(
			self.credentials, 
			self.SUBSCRIPTION_ID
		)
		self.network_client = NetworkManagementClient(
			self.credentials, 
			self.SUBSCRIPTION_ID
		)
		self.compute_client = ComputeManagementClient(
			self.credentials, 
			self.SUBSCRIPTION_ID
		)
		# instances holds all instance info
		self.instances = self.get_instances_info()
		# vm reference for create_instance
		self.VM_REFERENCE = {
			'linux': {
				'publisher': 'Canonical',
				'offer': 'UbuntuServer',
				'sku': '16.04.0-LTS',
				'version': 'latest'
			},
			'windows': {
				'publisher': 'MicrosoftWindowsServer',
				'offer': 'WindowsServer',
				'sku': '2016-Datacenter',
				'version': 'latest'
			}
		}
		# network
		self.VM_NAME = 'test6'
		self.VNET_NAME = 'guppi-vnet1'
		self.SUBNET_NAME = 'azure-sample-subnet10'
		self.IP_CONFIG_NAME = 'azure-sample-ip-config10'
		self.NIC_NAME = 'azure-sample-nic10'
	
	def check_setup(self):
		return True

	def create_instance(self):
		# randomize names
		self.VM_NAME = 'vm-' + str(random.randint(1,10000))
		self.VNET_NAME = 'vnet-' + str(random.randint(1,10000))
		self.SUBNET_NAME = 'subnet-' + str(random.randint(1,10000))
		self.IP_CONFIG_NAME = 'ip-config-' + str(random.randint(1,10000))
		self.NIC_NAME = 'nic-' + str(random.randint(1,10000))
		nic = self.create_nic(self.network_client)
		# Create Linux VM
		print('\nCreating Azure Instance...')
		vm_parameters = self.create_vm_parameters(nic.id, self.VM_REFERENCE['linux'])
		async_vm_creation = self.compute_client.virtual_machines.create_or_update(
            self.GROUP_NAME, self.VM_NAME, vm_parameters)
		async_vm_creation.wait()
		# recalibrate self.instances to reflect the change
		self.instances = self.get_instances_info()
		print("Azure Instance Created.")
		print("Rerun %guppi cloud to display.")

	def get_instances_info(self):
		vm_list = []
		instancesFormatted = []
		# get list of all active vms
		for vm in self.compute_client.virtual_machines.list_all():
			vm_list.append(vm.name)
		# make an info dict for each vm to display in accordian
		for vm_name in vm_list:
			key = ''
			vm = self.compute_client.virtual_machines.get(self.GROUP_NAME, vm_name, expand='instanceView')
			size = vm.hardware_profile.vm_size
			for disk in vm.instance_view.disks:
				for stat in disk.statuses:
					time = stat.time
			id = vm.id[-7:]
			name = vm.name
			
			zone = vm.location
			for stat in vm.instance_view.statuses:
				state = stat.display_status
			state = state.strip('VM ')
			formatInst = {
				'Name': name,
				'Instance Id': id,
				'Instance Type': size,
				'Availability Zone': zone,
				'State': state,
				'Key Name': key,
				'Launch Time': time,
			}
			instancesFormatted.append(formatInst)
		return instancesFormatted
  
	def terminate_instance(self,index):
		instances = self.get_instances_info()
		print("Terminating Azure Instance...")
		vm_name = instances[index]['Name']
		async_vm_delete = self.compute_client.virtual_machines.delete(self.GROUP_NAME, vm_name)
		async_vm_delete.wait()
		# recalibrate self.instances to reflect the change
		self.instances = self.get_instances_info()
		print("Azure Instance Terminated.")
		print("Rerun %guppi cloud to update.")

	def toggle_instance(self,index):
		instances = self.get_instances_info()
		current_state = instances[index]['State']
		if(current_state == "running"):
			print("Azure Instance Stopping...")
			async_vm_stop = self.compute_client.virtual_machines.power_off(self.GROUP_NAME, self.instances[index]['Name'])
			async_vm_stop.wait()
			# recalibrate self.instances to reflect the change
			self.instances = self.get_instances_info()
			print("Azure Instance Stopped.")
			print("Rerun %guppi cloud to update.")

		elif(current_state == "stopped"):
			print("Azure Instance Starting...")
			async_vm_start = self.compute_client.virtual_machines.start(self.GROUP_NAME, self.instances[index]['Name'])
			async_vm_start.wait()
			# recalibrate self.instances to reflect the change
			self.instances = self.get_instances_info()
			print("Azure Instance Started.")
			print("Rerun %guppi cloud to update.")

		else:
			print("Error: State is " + self.instances[index]['State'])

	def reboot_instance(self,index):
		print("Azure Instance Rebooting...")
		instances = self.get_instances_info()
		if(instances[index]['State'] == 'running'):
			vm_name = instances[index]['Name']
			async_vm_restart = self.compute_client.virtual_machines.restart(self.GROUP_NAME, vm_name)
			async_vm_restart.wait()
			# recalibrate self.instances to reflect the change
			self.instances = self.get_instances_info()
			print("Azure Instance Rebooted.")
			print("Rerun %guppi cloud to update.")
		else:
			print("Instance has already been toggled")
			print("Rerun %guppi cloud to reflect changes")

	
	def create_nic(self, network_client):
		# Create VNet
		print('\nCreating Vnet...')
		async_vnet_creation = self.network_client.virtual_networks.create_or_update(
			self.GROUP_NAME,
			self.VNET_NAME,
			{
				'location': self.LOCATION,
				'address_space': {
					'address_prefixes': ['10.0.0.0/16']
				}
			}
		)
		async_vnet_creation.wait()

		# Create Subnet
		print('\nCreating Subnet...')
		async_subnet_creation = network_client.subnets.create_or_update(
			self.GROUP_NAME,
			self.VNET_NAME,
			self.SUBNET_NAME,
			{'address_prefix': '10.0.0.0/24'}
		)
		subnet_info = async_subnet_creation.result()
		# Create NIC
		print('\nCreating NIC...')
		async_nic_creation = network_client.network_interfaces.create_or_update(
			self.GROUP_NAME,
			self.NIC_NAME,
			{
				'location': self.LOCATION,
				'ip_configurations': [{
					'name': self.IP_CONFIG_NAME,
					'subnet': {
						'id': subnet_info.id
					}
				}]
			}
		)
		return async_nic_creation.result()
	
	def create_vm_parameters(self, nic_id, vm_reference):
		# Create the VM parameters structure.
		return {
			'location': self.LOCATION,
			'os_profile': {
				'computer_name': self.VM_NAME,
				'admin_username': self.USERNAME,
				'admin_password': self.PASSWORD
			},
			'hardware_profile': {
				'vm_size': 'Standard_B1s'
			},
			'storage_profile': {
				'image_reference': {
					'publisher': vm_reference['publisher'],
					'offer': vm_reference['offer'],
					'sku': vm_reference['sku'],
					'version': vm_reference['version']
				},
			},
			'network_profile': {
				'network_interfaces': [{
					'id': nic_id,
				}]
			},
		}

	
if __name__ == '__main__':
	print('SubClass:', issubclass(MicrosoftService,
								PluginBase))
	print("Instance:", isinstance(MicrosoftService(),
								  PluginBase))