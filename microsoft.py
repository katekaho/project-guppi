from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute.models import DiskCreateOption

def get_credentials():
    credentials = ServicePrincipalCredentials(
        client_id = '1858e2f8-7a54-4898-be37-b922a72b737f',
        secret = 'jAzDkyVPFNfjF7QBPsgUr9/BynIhUQMeFCStbd3GE2A=',
        tenant = 'ad7ce373-aa8e-43d4-adab-480653dff4df'
    )

    return credentials

credentials = get_credentials()

SUBSCRIPTION_ID = '96c2b8eb-ed80-462e-901f-4047a240bae1'
GROUP_NAME = 'guppi'
LOCATION = 'westus'
VM_NAME = 'test1'

resource_group_client = ResourceManagementClient(
    credentials, 
    SUBSCRIPTION_ID
)
network_client = NetworkManagementClient(
    credentials, 
    SUBSCRIPTION_ID
)
compute_client = ComputeManagementClient(
    credentials, 
    SUBSCRIPTION_ID
)

def create_resource_group(resource_group_client):
    resource_group_params = { 'location':LOCATION }
    resource_group_result = resource_group_client.resource_groups.create_or_update(
        GROUP_NAME, 
        resource_group_params
    )
VM_LIST = []
print('\nList VMs in subscription')
for vm in compute_client.virtual_machines.list_all():
    print("\tVM: {}".format(vm.name))
    VM_LIST.append(vm.name)

def start_vm(VM_NAME):
# Start the VM
    print('\nStart VM')
    async_vm_start = compute_client.virtual_machines.start(GROUP_NAME, VM_NAME)
    async_vm_start.wait()

def restart_vm(VM_NAME):
# Restart the VM
    print('\nRestart VM')
    async_vm_restart = compute_client.virtual_machines.restart(GROUP_NAME, VM_NAME)
    async_vm_restart.wait()

def stop_vm(VM_NAME):
# Stop the VM
    print('\nStop VM')
    async_vm_stop = compute_client.virtual_machines.power_off(GROUP_NAME, VM_NAME)
    async_vm_stop.wait()

def terminate_vm(VM_NAME):
# Delete VM
    print('\nDelete VM')
    async_vm_delete = compute_client.virtual_machines.delete(GROUP_NAME, VM_NAME)
    async_vm_delete.wait()

def get_vm(compute_client):
    vm = compute_client.virtual_machines.get(GROUP_NAME, VM_NAME, expand='instanceView')
    print("hardwareProfile")
    print("   vmSize: ", vm.hardware_profile.vm_size)
    print("\nstorageProfile")
    print("  imageReference")
    print("    publisher: ", vm.storage_profile.image_reference.publisher)
    print("    offer: ", vm.storage_profile.image_reference.offer)
    print("    sku: ", vm.storage_profile.image_reference.sku)
    print("    version: ", vm.storage_profile.image_reference.version)
    print("  osDisk")
    print("    osType: ", vm.storage_profile.os_disk.os_type.value)
    print("    name: ", vm.storage_profile.os_disk.name)
    print("    createOption: ", vm.storage_profile.os_disk.create_option)
    print("    caching: ", vm.storage_profile.os_disk.caching.value)
    print("\nosProfile")
    print("  computerName: ", vm.os_profile.computer_name)
    print("  adminUsername: ", vm.os_profile.admin_username)
    print("\nnetworkProfile")
    for nic in vm.network_profile.network_interfaces:
        print("  networkInterface id: ", nic.id)
    print("\nvmAgent")
    print("  vmAgentVersion", vm.instance_view.vm_agent.vm_agent_version)
    print("    statuses")
    for stat in vm.instance_view.vm_agent.statuses:
        print("    code: ", stat.code)
        print("    displayStatus: ", stat.display_status)
        print("    message: ", stat.message)
        print("    time: ", stat.time)
    print("\ndisks");
    for disk in vm.instance_view.disks:
        print("  name: ", disk.name)
        print("  statuses")
        for stat in disk.statuses:
            print("    code: ", stat.code)
            print("    displayStatus: ", stat.display_status)
            print("    time: ", stat.time)
    print("\nVM general status")
    print("  provisioningStatus: ", vm.provisioning_state)
    print("  id: ", vm.id)
    print("  name: ", vm.name)
    print("  type: ", vm.type)
    print("  location: ", vm.location)
    print("\nVM instance status")
    for stat in vm.instance_view.statuses:
        print("  code: ", stat.code)
        print("  displayStatus: ", stat.display_status)

get_vm(compute_client)