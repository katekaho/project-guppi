from pluginbase import Google
from googleapiclient.discovery import build
import os

class LocalBaseClass:
  pass

@Google.register
class GoogleService(LocalBaseClass):
  
  def create_instance(self, compute, project, zone, name):
    # Get the latest Debian Jessie image.
    image_response = compute.images().getFromFamily(
        project='debian-cloud', family='debian-9').execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone

    config = {
        'name': name,
        'machineType': machine_type,

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
    compute.instances().insert(project=project, zone=zone, body=config).execute()
    print("Instance Created.")
    print("Rerun %db to display.")

  def get_instances_info(self, compute, project, zone):
    instances = compute.instances().list(project=project, zone=zone).execute()

    instancesFormatted = []
    
    instances = instances.get('items', '')
       
    for instance in instances:
        
        machineType = instance.get('machineType', '').rsplit('/', 1)[-1]
        
        zone = instance.get('zone', '').rsplit('/', 1)[-1]
        
        formatInst = {
            'Name': instance.get('name', ''),
            'Instance Id': instance.get('id', ''),
            'Instance Type': machineType,
            'Availability Zone': zone,
            'State': instance.get('status', ''),
            'Key Name': '',
            'Launch Time': instance.get('creationTimestamp', ''),
        }
        
        instancesFormatted.append(formatInst)
        
    return instancesFormatted

  
    
