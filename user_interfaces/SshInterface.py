from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display, FileLink
import ipywidgets as widgets

import plugins
import paramiko



#===================================================#
#--------------SSH-Interface-Function---------------#
#===================================================#
def render_ssh_interface(cloud_list):
	box_layout = widgets.Layout(
				border='solid 1px',
				# padding='0.5em',
				margin='0.5em',
				width = '28%',
				
			)
	instances = cloud_list[0].get_instances_info()
	box_list = []
	instance_boxes = []

	

	for vm in instances:
		
		if(vm['State'] == 'running'):


			if(vm['Name'] == ''):	
				cb = widgets.Checkbox(
					value=False,
					description=vm['Instance Id'],
					disabled=False
				)
			else:
				cb = widgets.Checkbox(
					value=False,
					description=vm['Name'],
					disabled=False
				)
			instance_boxes.append(widgets.Box([cb], layout=box_layout))
			box_list.append(cb)

	select_button = widgets.Button(
		description='Select All',
		disabled=False,
		tooltip='',
		icon='check',

	)	
	display(select_button)


	box_array = []
	for i in range(0, len(instance_boxes), 3):
		box_array.append(instance_boxes[i:i+3])
	
	for row in box_array:
		boxes_container = widgets.HBox(row)

		display(boxes_container)
	
	command_area = widgets.Textarea(
		value='',
		placeholder='Type your commands here',
	)

	submit_button = widgets.Button(
		description='Run Commands',
		disabled=False,
		tooltip='',
	)
	command_box = widgets.VBox([command_area,submit_button])
	display(command_box)

	# submit button clicked function
	def submit_button_clicked(b):
		for checkbox in box_list:
			if(checkbox.value == True):
				print("=======================================================")
				print(checkbox.description)
				print("=======================================================")
				Dns = ''
				for vm in instances:
					if(checkbox.description == vm['Instance Id'] or checkbox.description == vm['Name']):
						Dns = vm['Dns']
				ssh = paramiko.SSHClient()
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				ssh.connect(Dns,
						username='ec2-user',
						key_filename='key.pem')
				commands = command_area.value
			
				stdin, stdout, stderr = ssh.exec_command(commands)
				stdin.flush()
				data = stdout.read().splitlines()
				for output_line in data:
					print(output_line)
				ssh.close()
				print("")
				print("")

	
	# select button clicked function
	def select_button_clicked(b):
		toggle = check_true(box_list)
		for checkbox in box_list:
			checkbox.value = toggle

	def check_true(box_list):
		if(box_list[0].value):
			for box in box_list:
				if(not box.value):
					return True
			return False
		else:
			for box in box_list:
				if(box.value):
					return True
			return True

	submit_button.on_click(submit_button_clicked)
	select_button.on_click(select_button_clicked)