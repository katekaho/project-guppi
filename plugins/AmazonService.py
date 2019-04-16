from pluginbase import PluginBase
import boto3 

class LocalBaseClass:
	pass
@PluginBase.register
class AmazonService(LocalBaseClass):
	def __init__(self):
		self.type = "AWS SERVICE"
		self.ec2 = boto3.resource('ec2')
		self.ec2_client = boto3.client('ec2')
		self.formatted_instances = self.get_instances_info()
	
	def check_setup(self):
		return True
		
	def create_instance(self):
		self.ec2.create_instances(
			ImageId='ami-082c116bf79a9feef',
			MinCount=1,
			MaxCount=1,
			InstanceType='t2.micro',
			KeyName='new_key_pair',
		)
		print("Instance Created.")
		print("Rerun %guppi cloud to display.")
	
	def get_instances_info(self):
		response = self.ec2_client.describe_instances()
		reservations = response.get('Reservations')
		instances = []

		for reservation in reservations:
			reservationInstances = reservation.get('Instances')
			for inst in reservationInstances:
				instances.append(inst)

		instancesFormatted = []

		for instance in instances:
			tags = instance.get('Tags', [])
			name = ''
			for tag in tags:
				tagKey = tag.get('Key', '')
				if tagKey == 'Name':
					name = tag['Value']

			placement = instance['Placement']
			availabilityZone = placement['AvailabilityZone']

			state = instance['State']
			stateName = state.get('Name', '')

			launchTime = instance.get('LaunchTime', '')

			if len(name) > 20:
				name = name[:20] + '...'

			formatInst = {
				'Name': name,
				'Instance Id': instance.get('InstanceId', ''),
				'Instance Type': instance.get('InstanceType', ''),
				'Availability Zone': availabilityZone,
				'State': stateName,
				'Key Name': instance.get('KeyName', ''),
				'Launch Time': launchTime,
			}
			instancesFormatted.append(formatInst)

		return instancesFormatted
  
	def terminate_instance(self,index):
		print("Terminating AWS Instance...")
		instances = self.get_instances_info()
		ids = [instances[index]['Instance Id']]
		self.ec2.instances.filter(InstanceIds=ids).terminate()
		# recalibrate self.formatted_instances to reflect the change
		self.formatted_instances = self.get_instances_info()
		print("AWS Instance Terminated.")
		print("Rerun %guppi cloud to update.")

	def toggle_instance(self,index):
		instances = self.get_instances_info()
		ids = [instances[index]['Instance Id']]

		current_state = instances[index]['State']
		if(current_state == "running"):
			print("Stopping AWS nstance...")
			self.ec2.instances.filter(InstanceIds=ids).stop()
			print("AWS Instance Stopped.")
			print("Rerun %guppi cloud to update.")

		elif(current_state == "stopped"):
			print("Starting AWS Instance...")
			self.ec2.instances.filter(InstanceIds=ids).start()
			print("AWS Instance Started.")
			print("Rerun %guppi cloud to update.")
		else:
			print("Instance has already been toggled")
			print("Rerun %guppi cloud to reflect changes")
		# recalibrate self.formatted_instances to reflect the change
		self.formatted_instances = self.get_instances_info()

	def reboot_instance(self,index):
		print("Rebooting AWS Instance...")
		instances = self.get_instances_info()
		state = instances[index]['State']
		if(state == "running"):
			ids = [instances[index]['Instance Id']]
			self.ec2.instances.filter(InstanceIds=ids).reboot()
			# recalibrate self.formatted_instances to reflect the change
			self.formatted_instances = self.get_instances_info()
			print("AWS Instance Rebooted.")
			print("Rerun %guppi cloud to update.")
		else:
			print("Please rerun %guppi cloud to reflect changes")
			print("You can only reboot instances that are  \"Running\" ")
	
if __name__ == '__main__':
	print('SubClass:', issubclass(AmazonService,
								PluginBase))
	print("Instance:", isinstance(AmazonService(),
								  PluginBase))