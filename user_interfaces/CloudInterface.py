from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display, FileLink, clear_output
import ipywidgets as widgets
from ipywidgets import Layout, Button, Box, FloatText, Textarea, Dropdown, Label, IntSlider

#===================================================#
#--------------SSH-Interface-Function---------------#
#===================================================#
def render_cloud_interface(cloud_list, cloud_index):
	service = cloud_list[cloud_index]
	service_name = service.type
	if(cloud_index < 0):
		service_name = "MultiCloud"
	title = widgets.HTML("<h4>"+service_name+" Instances</h4>")
	display(title)
	instances = []
	if(cloud_index < 0):
		for cloud in cloud_list:
			inst_info = cloud.get_instances_info()
			ind = 0
			for info in inst_info:
				info['index'] = ind
				instances.append(info)
				ind+=1
	else:
		instances = cloud_list[cloud_index].get_instances_info()

	group_list = []
	# print(instances)
	for instance in instances:
		group_name = instance['Group Name']
		if group_name not in group_list and group_name != '':
			group_list.append(group_name)

	group_list.sort(key=str.lower)
	tab_arr = []
	layout_arr = render_group(service,instances,'All Instances', cloud_list)
	
	tab_child = widgets.VBox(layout_arr)
	tab_arr.append(tab_child)

	if(cloud_index < 0):
		a_instances = instances[0:len(cloud_list[0].get_instances_info())]
		g_instances = instances[len(cloud_list[0].get_instances_info()) : len(instances)]
		a_layout_arr =  render_group(service,a_instances,'Amazon Instances', cloud_list)
		g_layout_arr =  render_group(service,g_instances,'Google Instances', cloud_list)
		tab_child1 = widgets.VBox(a_layout_arr)
		tab_child2 = widgets.VBox(g_layout_arr)

		tab_arr.append(tab_child1)
		tab_arr.append(tab_child2)


	tab = widgets.Tab()
	for group_name in group_list:
		layout_arr = render_group(service,instances,group_name, cloud_list)
		tab_child = widgets.VBox(layout_arr)
		tab_arr.append(tab_child)
	
	tab.children = tab_arr
	tab.set_title(0,'All Instances')
	offset = 1
	if(cloud_index < 0):
		tab.set_title(1,"Amazon Instances")
		tab.set_title(2,"Google Instances")
		offset = 3
	# set titles for tab
	for i in range(len(group_list)):
		tab.set_title(i+offset, group_list[i])

	display(tab)
	

def render_group(service,instances, group_name, cloud_list):
	group_widget_list = []

	accordion_children = []
	index = 0

	for instance in instances:
		if(instance['Group Name'] == group_name or group_name == 'All Instances' or group_name == "Amazon Instances" or group_name == "Google Instances"):
			accordion_child = render_instance_info(service, instance, index, instances, cloud_list)
			accordion_children.append(accordion_child)
		index += 1

	accordion = widgets.Accordion(accordion_children)

	acc_index = 0
				
	#adding titles to the accordian
	for row in instances:
		if(row['Group Name'] == group_name or group_name == 'All Instances'or group_name == "Amazon Instances" or group_name == "Google Instances"):
			acc_title = row['Instance Id']
			acc_title += " | "
			if group_name == 'All Instances' or group_name == "Amazon Instances" or group_name == "Google Instances":
				acc_title += row['Group Name']
				acc_title += " | "
			acc_title += row['State']
			acc_title += " | "
			acc_title += row['Service']
			
			accordion.set_title(acc_index, acc_title)
			acc_index += 1

	group_widget_list.append(accordion)

	return group_widget_list

def render_instance_info(service, instance_info, index, instances, cloud_list):
	

	#appends all info into array of labels
	info1 = ["<b>Instance Type:</b>", instance_info['Instance Type'] ,"<b>Availability Zone:</b>", instance_info['Availability Zone'],"<b>Group:<b>"]

	info2 = ["<b>State:<b>" , instance_info['State'], "<b>Public DNS:<b>", instance_info['Dns']]

	#makes each label html and puts into HBox
	items1 = [widgets.HTML(str(i)) for i in info1]
	

	items2 = [widgets.HTML(str(i)) for i in info2]
	instance_info2 = widgets.HBox(items2)

	group_list = []

	for instance in instances:
		if instance['Group Name'] not in group_list:
			group_list.append(instance['Group Name'])
	
	#group dropdown
	group_dropdown = widgets.Dropdown(
		options = group_list,
		value=instance_info['Group Name'],
		disabled=False,
		layout=widgets.Layout(width='20%'),
	)
	items1.append(group_dropdown)

	

	instance_info1 = widgets.HBox(items1)

	instance_list = []
	instance_list.append(instance_info['Instance Id'])

	

	

	#buttons
	if(instance_info['State'] == "running"): 
		toggle_button = widgets.Button(description='Stop Instance')
	elif(instance_info['State'] == "stopped"):
		toggle_button = widgets.Button(description='Start Instance')
	else:
		toggle_button = widgets.Button(description='Start Instance',disabled=True)

	#disables the terminate button when not running or stopped
	if(instance_info['State'] == "running" or instance_info['State'] == "stopped"):
		terminate_button = widgets.Button(description='Terminate Instance')
	else:
		terminate_button = widgets.Button(description='Terminate Instance',disabled=True)
	# reboot button
	if(instance_info['State'] == "running"):
		reboot_button = widgets.Button(description='Reboot Instance')
	else:
		reboot_button = widgets.Button(description='Reboot Instance',disabled=True)


	file = open("icons/running.png", "rb")

	if(instance_info['State'] == "running"):
		file = open("icons/running.png", "rb")
	elif(instance_info['State'] == "pending"or instance_info['State'] == 'staging'):
		file = open("icons/pending.png", "rb")
	elif(instance_info['State'] == "stopping"):
		file = open("icons/stopping.png", "rb")
	elif(instance_info['State'] == "stopped"):
		file = open("icons/stopped.png", "rb")
	elif(instance_info['State'] == "shutting-down"):
		file = open("icons/shutting-down.png", "rb")
	else:
		file = open("icons/terminated.png", "rb")

	image = file.read()
	indicator = widgets.Image(value=image,format='png')

	buttons = [toggle_button,reboot_button,terminate_button,indicator]
	button_box = widgets.HBox(buttons)

	#puts info and buttons into vBox
	instance_box = widgets.VBox([instance_info1, instance_info2, button_box])

	#===================================================#
	#-----------------Button-Functions------------------#
	#===================================================#
	#terminate instance button handler
	def terminate_button_clicked(b):
		if(instance_info['Service'] == "Amazon"):
			cloud_list[0].terminate_instance(instance_info['index'])
		else:
			cloud_list[1].terminate_instance(instance_info['index'])
		# refresh cell
		# clear_output()
		# render_cloud_interface(cloud_list, 0)


	#toggle instance button handler
	def toggle_button_clicked(b):
		# service.toggle_instance(index)
		if(instance_info['Service'] == "Amazon"):
			cloud_list[0].toggle_instance(instance_info['index'])
		else:
			cloud_list[1].toggle_instance(instance_info['index'])
		# refresh cell
		# clear_output()
		# render_cloud_interface(cloud_list, 0)

	#reboot instance button handler
	def reboot_button_clicked(b):
		# service.reboot_instance(index)
		if(instance_info['Service'] == "Amazon"):
			cloud_list[0].reboot_instance(instance_info['index'])
		else:
			cloud_list[1].reboot_instance(instance_info['index'])
		# refresh cell
		# clear_output()
		# render_cloud_interface(cloud_list, 0)

	def on_change(change):
		service.update_group(instance_list, group_dropdown.value)
		print("Changed group to " + group_dropdown.value)
		print("Rerun %guppi cloud to display")

	group_dropdown.observe(on_change, names='value')

	toggle_button.on_click(toggle_button_clicked)
	terminate_button.on_click(terminate_button_clicked)
	reboot_button.on_click(reboot_button_clicked)

	return instance_box