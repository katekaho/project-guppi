from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute.models import DiskCreateOption
from pluginbase import PluginBase

class LocalBaseClass:
	pass
@PluginBase.register
class MicrosoftService(LocalBaseClass):
	def __init__(self):
		self.type = "AZURE SERVICE"
		self.client_id = '1858e2f8-7a54-4898-be37-b922a72b737f'
		self.secret = 'jAzDkyVPFNfjF7QBPsgUr9/BynIhUQMeFCStbd3GE2A='
		self.tenant = 'ad7ce373-aa8e-43d4-adab-480653dff4df'
		self.SUBSCRIPTION_ID = '96c2b8eb-ed80-462e-901f-4047a240bae1'
		self.GROUP_NAME = 'guppi'
		self.LOCATION = 'westus'
		self.VM_NAME = 'test1'
		self.credentials = ServicePrincipalCredentials(
			client_id = self.client_id,
			secret = self.secret,
			tenant = self.tenant
		)
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

	def create_instance(self):
		self.ec2.create_instances(
			ImageId='ami-0799ad445b5727125',
			MinCount=1,
			MaxCount=1,
			InstanceType='t2.micro',
			KeyName='key_pair_guppi',
		)
		print("Instance Created.")
		print("Rerun %db to display.")
	
	def get_instances_info(self):
		vm_list = []
		instancesFormatted = []
		for vm in self.compute_client.virtual_machines.list_all():
			vm_list.append(vm.name)
		for vm_name in vm_list:
			key = ''
			vm = self.compute_client.virtual_machines.get(self.GROUP_NAME, vm_name, expand='instanceView')
			size = vm.hardware_profile.vm_size
			for disk in vm.instance_view.disks:
				for stat in disk.statuses:
					time = stat.time
			id = vm.id
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
		instances = self.formatted_instances
		ids = [instances[index]['Instance Id']]
		self.ec2.instances.filter(InstanceIds=ids).terminate()
		print("Instance Terminated.")
		print("Rerun %db to update.")

	def toggle_instance(self,index):
		async_vm_stop = self.compute_client.virtual_machines.power_off(self.GROUP_NAME, self.VM_NAME)
		async_vm_stop.wait()
		# instances = self.formatted_instances
		# ids = [instances[index]['Instance Id']]

		# current_state = instances[index]['State']
		# if(current_state == "running"):
		# 	self.ec2.instances.filter(InstanceIds=ids).stop()
		# 	print("Instance Stopped.")
		# 	print("Rerun %db to update.")

		# elif(current_state == "stopped"):
		# 	self.ec2.instances.filter(InstanceIds=ids).start()
		# 	print("Instance Started.")
		# 	print("Rerun %db to update.")



	def reboot_instance(self,index):
		instances = self.formatted_instances
		ids = [instances[index]['Instance Id']]
		self.ec2.instances.filter(InstanceIds=ids).reboot()
		print("Instance Rebooted.")
		print("Rerun %db to update.")
	
if __name__ == '__main__':
	print('SubClass:', issubclass(AmazonService,
								PluginBase))
	print("Instance:", isinstance(AmazonService(),
								  PluginBase))