from pluginbase import PluginBase
from googleapiclient.discovery import build

class LocalBaseClass:
  pass

@PluginBase.register
class GoogleService(LocalBaseClass):
  
  def get_instances_info(self, compute, project, zone):
    # compute = build('compute', 'v1')
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

    
