from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display
import boto3 
import ipywidgets as widgets

def on_button_clicked(b):
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
    print("Rerun %db magic to display.")

@magics_class
class TestMagics(Magics):
    @line_magic
    def db(self, line):
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
        button = widgets.Button(description="Create Instance")
        display(button)
        button.on_click(on_button_clicked)


        # children = []
        # # children = [widgets.Text(description=instance['Instance Id']) for instance in instancesFormatted]
        # for instance in instancesFormatted:
        #     children.append(
        #                     widgets.HTML(
        #                         value="""<table>
        #                                     <tr>
        #                                         <th>
        #                                             Name &emsp;
        #                                         </th>
        #                                         <th>
        #                                             Instance ID &emsp;
        #                                         </th>
        #                                         <th>
        #                                             Instance Type &emsp;
        #                                         </th>
        #                                         <th>
        #                                             Availability Zone&emsp;
        #                                         </th>
        #                                         <th>
        #                                             State &emsp;
        #                                         </th>
        #                                         <th>
        #                                             Key Name &emsp;
        #                                         </th>
        #                                         <th>
        #                                             LaunchTime 
        #                                         </th>
        #                                     </tr>
        #                                 <table>""",
        #                         placeholder='Some HTML',
        #                     )
        #     )
    
        # tab = widgets.Tab()
        # tab.children = children
        # count = 0
        # for instance in instancesFormatted:
        #     tab.set_title(count,instance['Instance Id'])
        #     count+=1

        # # for i in range(len(children)):
        # #     tab.set_title(i, str(i))
        # display(tab)

def load_ipython_extension(ipython):
    """This function is called when the extension is
    loaded. It accepts an IPython InteractiveShell
    instance. We can register the magic with the
    `register_magic_function` method of the shell
    instance."""
    ipython.register_magics(TestMagics)
