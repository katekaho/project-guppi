from pluginbase import PluginBase
import boto3 

class LocalBaseClass:
    pass
@PluginBase.register
class AmazonService(LocalBaseClass):
    def __init__(self):
        self.ec2 = boto3.resource('ec2')
        self.ec2_client = boto3.client('ec2')
        self.formatted_instances = self.get_instances_info()
        
    def create_instance(self):
        self.ec2.create_instances(
            #ImageId='ami-0cd3dfa4e37921605', #kates ami
            ImageId='ami-0799ad445b5727125', #joeys ami
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName='key_pair_guppi',
        )
        print("Instance Created.")
        print("Rerun %db to display.")
    
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
        instances = self.formatted_instances
        ids = [instances[index]['Instance Id']]
        self.ec2.instances.filter(InstanceIds=ids).terminate()
        print("Instance Terminated.")
        print("Rerun %db to update.")

    def toggle_instance(self,index):
        instances = self.formatted_instances
        ids = [instances[index]['Instance Id']]

        current_state = instances[index]['State']
        if(current_state == "running"):
            self.ec2.instances.filter(InstanceIds=ids).stop()
            print("Instance Stopped.")
            print("Rerun %db to update.")

        elif(current_state == "stopped"):
            self.ec2.instances.filter(InstanceIds=ids).start()
            print("Instance Started.")
            print("Rerun %db to update.")

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