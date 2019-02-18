from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display
import boto3 
import ipywidgets as widgets

selected_instance = ""
accordion =""
#create instance button handler
def create_button_clicked(b):
    ec2 = boto3.resource('ec2')
    ec2.create_instances(
      #ImageId='ami-0cd3dfa4e37921605', #kates ami
      ImageId='ami-0799ad445b5727125', #joeys ami
      MinCount=1,
      MaxCount=1,
      InstanceType='t2.micro',
      KeyName='key_pair_guppi',
    )
    print("Instance Created.")
    print("Rerun %db to display.")

#terminate instance button handler
def terminate_button_clicked(b):
    global selected_instance
    global accordion
    selected_instance = accordion.selected_index
    ec2 = boto3.resource('ec2')
    instances = get_instances_info()
    ids = [instances[selected_instance]['Instance Id']]
    ec2.instances.filter(InstanceIds=ids).terminate()
    print("Instance Terminated.")
    print("Rerun %db to update.")

#toggle instance button handler
def toggle_button_clicked(b):
    global selected_instance
    global accordion
    selected_instance = accordion.selected_index
    ec2 = boto3.resource('ec2')
    instances = get_instances_info()
    ids = [instances[selected_instance]['Instance Id']]
    
    if(instances[selected_instance]['State'] == "running"):
        ec2.instances.filter(InstanceIds=ids).stop()
        print("Instance Stopped.")
        print("Rerun %db to update.")
    elif(instances[selected_instance]['State'] == "stopped"):
        ec2.instances.filter(InstanceIds=ids).start()
        print("Instance Started.")
        print("Rerun %db to update.")
    

def get_instances_info():
    ec2client = boto3.client('ec2')
    response = ec2client.describe_instances()
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

@magics_class
class TestMagics(Magics):
    @line_magic
    def db(self, line):
        global selected_instance
        global accordion
        ec2client = boto3.client('ec2')
        response = ec2client.describe_instances()
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
        button = widgets.Button(description="Create Instance")
        display(button)
        button.on_click(create_button_clicked)

        if(line == "table"):
            html = "<table><tr>"
            html += "<th>"
            html += 'Name'
            html += "</th>"
            html += "<th>"
            html += 'Instance Id'
            html += "</th>"
            html += "<th>"
            html += 'Instance Type'
            html += "</th>"
            html += "<th>"
            html += 'Availability Zone'
            html += "</th>"
            html += "<th>"
            html += 'State'
            html += "</th>"
            html += "<th>"
            html += 'Key Name'
            html += "</th>"
            html += "<th>"
            html += 'Launch Time'
            html += "</th>"
            html += "</tr>"
            for row in instancesFormatted:
                html += "<tr>"
                html += "<td>"
                html += row['Name']
                html += "</td>"
                html += "<td>"
                html += row['Instance Id']
                html += "</td>"
                html += "<td>"
                html += row['Instance Type']
                html += "</td>"
                html += "<td>"
                html += row['Availability Zone']
                html += "</td>"
                html += "<td>"
                html += row['State']
                html += "</td>"
                html += "<td>"
                html += row['Key Name']
                html += "</td>"
                html += "<td>"
                html += str(row['Launch Time'])
                html += "</td>"
                html += "</tr>"
            html += "</table>"
            display(HTML(html))
         
        else:
            #stores the info and buttons for each instance
            accordion_children = []

            for row in instancesFormatted:
                #appends all info into array of labels
                info = ["<b>Instance Type:</b>", row['Instance Type'] ,"<b>Availability Zone:</b>", row['Availability Zone'], "<b>State:<b>" , row['State']]

                #makes each label html and puts into HBox
                items = [widgets.HTML(str(i)) for i in info]
                instance_info = widgets.HBox(items)

                #buttons
                
                if(row['State'] == "running"):
                    toggle_button = widgets.Button(description='Stop Instance')
                elif(row['State'] == "stopped"):
                    toggle_button = widgets.Button(description='Start Instance')
                else:
                    toggle_button = widgets.Button(description='Start Instance',disabled=True)

                #disables the terminate button when not running or stopped
                if(row['State'] == "running" or row['State'] == "stopped"):
                    terminate_button = widgets.Button(description='Terminate Instance')
                else:
                    terminate_button = widgets.Button(description='Terminate Instance',disabled=True)

                indicator=widgets.IntProgress(value=1,min=0,max=1,bar_style='danger') #red
                # 'success', 'info', 'warning', 'danger' or ''

                if(row['State'] == "running"):
                    indicator.bar_style = 'success'
                elif(row['State'] == "pending"):
                    indicator.bar_style = ''
                elif(row['State'] == "stopping" or row['State'] == "shutting-down"):
                    indicator.bar_style = 'warning'
                else:
                    indicator.bar_style = 'danger'
                

                toggle_button.on_click(toggle_button_clicked)
                terminate_button.on_click(terminate_button_clicked)

                buttons = [toggle_button,terminate_button,indicator]
                button_box = widgets.HBox(buttons)

                
                #puts info and buttons into vBox
                instance_box = widgets.VBox([instance_info, button_box])

                #adds it to list of childeren for accordian
                accordion_children.append(instance_box)

            accordion = widgets.Accordion(accordion_children)

            acc_index = 0
            
            #adding titles to the accordian
            for row in instancesFormatted:
                acc_title = row['Instance Id']
                acc_title += " "
                acc_title += row['State']
                accordion.set_title(acc_index, acc_title)
                acc_index += 1

            display(accordion)

            
            #sets global selected instance to currently selected instance
            selected_instance = accordion.selected_index
        

        

        

def load_ipython_extension(ipython):
    """This function is called when the extension is
    loaded. It accepts an IPython InteractiveShell
    instance. We can register the magic with the
    `register_magic_function` method of the shell
    instance."""
    ipython.register_magics(TestMagics)
