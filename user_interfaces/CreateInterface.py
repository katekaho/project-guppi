from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display, FileLink
import ipywidgets as widgets

import plugins
import paramiko
import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')


#===================================================#
#--------------Create-Interface-Function------------#
#===================================================#
def render_create_interface(cloud_list):

	service = cloud_list[0]

	instances = service.get_instances_info()

	group_list = ["Create Group"]

	for instance in instances:
		group_name = instance['Group Name']
		if group_name not in group_list and group_name != '':
			group_list.append(group_name)

	group_list.sort(key=str.lower)

	group_dropdown = widgets.Dropdown(
		options = group_list,
		description= "Group: ",
	)
	
	new_group_text = widgets.Text(
		value= '',
		placeholder= 'New Group Name',
		disabled = False
	)

	def on_change(change):
		if(group_dropdown.value == "Create Group"):
			new_group_text.disabled = False
		else:
			new_group_text.disabled = True

	group_dropdown.observe(on_change)

	name_row_arr = [group_dropdown,new_group_text]

	name_row = widgets.HBox(name_row_arr)
	display(name_row)

	size_list = ['t2.nano', 't2.micro', 't2.small', 't2.small', 't2.medium', 't2.large', 't2.xlarge', 't2.2xlarge', 't3.nano', 't3.micro', 't3.small', 't3.medium', 't3.large', 't3.xlarge', 't3.2xlarge', 'm5d.large', 'm5d.xlarge', 'm5d.2xlarge', 'm5d.4xlarge', 'm5d.12xlarge', 'm5d.24xlarge',  'm5.large', 'm5.xlarge', 'm5.2xlarge', 'm5.4xlarge', 'm5.12xlarge', 'm5.24xlarge', 'm4.large', 'm4.xlarge', 'm4.2xlarge', 'm4.4xlarge', 'm4.10xlarge', 'm4.16xlarge', 'c5d.large', 'c5d.xlarge', 'c5d.2xlarge', 'c5d.4xlarge', 'c5d.9xlarge', 'c5d.18xlarge', 'c5.large', 'c5.xlarge', 'c5.2xlarge', 'c5.4xlarge', 'c5.9xlarge', 'c5.18xlarge', 'c4.large', 'c4.xlarge', 'c4.2xlarge', 'c4.4xlarge', 'c4.8xlarge', 'g2.2xlarge', 'g2.8xlarge', 'g3.4xlarge', 'g3.8xlarge', 'g3.16xlarge', 'r5d.large', 'r5d.xlarge', 'r5d.2xlarge', 'r5d.4xlarge', 'r5d.12xlarge', 'r5.large', 'r5.xlarge', 'r5.2xlarge', 'r5.4xlarge', 'r5.12xlarge', 'r5.24xlarge', 'r4.large', 'r4.xlarge', 'r4.2xlarge', 'r4.4xlarge', 'r4.8xlarge', 'r4.16xlarge', 'z1d.large', 'z1d.xlarge', 'z1d.2xlarge', 'z1d.3xlarge', 'z1d.6xlarge', 'z1d.12xlarge', 'd2.xlarge', 'd2.2xlarge', 'd2.4xlarge', 'd2.8xlarge', 'i2.xlarge', 'i2.2xlarge', 'i2.4xlarge', 'i2.8xlarge', 'i3.large', 'i3.xlarge', 'i3.2xlarge', 'i3.4xlarge', 'i3.8xlarge', 'i3.16xlarge', 'i3.metal']

	size_dropdown = widgets.Dropdown(
		options = size_list,
		description= "Size: ",
		value = 't2.micro',
	)

	create_button = widgets.Button(
		description='Create Instance'
	)



	def create_button_clicked(b):
		if(new_group_text.value == '' and group_dropdown.value == 'Create Group'):
			print("Please enter a group name")
		else:
			# def create_instance(self,group,size,region):
			group = group_dropdown.value

			if(group == "Create Group"):
				group = new_group_text.value

			service.create_instance(group,size_dropdown.value)
		

	create_button.on_click(create_button_clicked)

	size_region_row = [size_dropdown,create_button]
	sr_row = widgets.HBox(size_region_row)
	display(sr_row)





