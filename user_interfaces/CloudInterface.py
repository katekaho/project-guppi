from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display, FileLink
import ipywidgets as widgets
import plugins

import webbrowser

#===================================================#
#------------Cloud-Interface-Function---------------#
#===================================================#
def render_cloud_interface(cloud_list):

	cloud_arr = cloud_list
	tab_list = []
	accordion_arr = []

	for cloud_service in cloud_list:

		type_label = widgets.HTML(value="<b>"+cloud_service.type+"<b>")

		button = widgets.Button(description="Create Instance")
		toggle_button = widgets.Button(description='Stop Instance')
		terminate_button = widgets.Button(description='Terminate Instance')
		reboot_button = widgets.Button(description='Reboot Instance',disabled=True)
		accordion = widgets.Accordion()
		tab_nest = widgets.Tab()
		service = ''


		if(cloud_service.check_setup() == False):	
			accordion = widgets.Accordion([])
			fn = "./"+cloud_service.name +"Setup.txt"
			html_as_str = open(fn, 'r').read()
			setup = widgets.HTML(value=html_as_str)
			button_and_title = widgets.VBox([setup])
			
		else:
			instancesFormatted = cloud_service.get_instances_info()
			# display(type_label)
			button = widgets.Button(description="Create Instance")
			# display(button)
			button_and_title = widgets.VBox([type_label,button])

			#stores the info and buttons for each instance
			accordion_children = []
			if (len(instancesFormatted) == 0):
				accordion = widgets.Accordion([])
				message = widgets.HTML(value="No instances found, press 'Create Instance' to create one")
				button_and_title = widgets.VBox([type_label,message,button])
			else:
				for row in instancesFormatted:
					#appends all info into array of labels
					info = ["<b>Instance Type:</b>", row['Instance Type'] ,"<b>Availability Zone:</b>", row['Availability Zone'], "<b>State:<b>" , row['State'], "<b>Public DNS:<b>", row['Dns']]

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
					# reboot button
					if(row['State'] == "running"):
						reboot_button = widgets.Button(description='Reboot Instance')
					else:
						reboot_button = widgets.Button(description='Reboot Instance',disabled=True)


					file = open("icons/running.png", "rb")

					if(row['State'] == "running"):
						file = open("icons/running.png", "rb")
					elif(row['State'] == "pending"or row['State'] == 'staging'):
						file = open("icons/pending.png", "rb")
					elif(row['State'] == "stopping"):
						file = open("icons/stopping.png", "rb")
					elif(row['State'] == "stopped"):
						file = open("icons/stopped.png", "rb")
					elif(row['State'] == "shutting-down"):
						file = open("icons/shutting-down.png", "rb")
					else:
						file = open("icons/terminated.png", "rb")

					image = file.read()
					indicator = widgets.Image(value=image,format='png')

					buttons = [toggle_button,reboot_button,terminate_button,indicator]
					button_box = widgets.HBox(buttons)
					
					#puts info and buttons into vBox
					instance_box = widgets.VBox([instance_info, button_box])

					#adds it to list of childeren for accordian
					accordion_children.append(instance_box)
					#===================================================#
					#-----------------Button-Functions------------------#
					#===================================================#

					selected_instance = ''

					def create_button_clicked(b):
						service = cloud_arr[selected_service]
						service.create_instance()

					#terminate instance button handler
					def terminate_button_clicked(b):
						service = cloud_arr[selected_service]
						accordion = accordion_arr[selected_service]
						selected_instance = accordion.selected_index
						service.terminate_instance(selected_instance)


					#toggle instance button handler
					def toggle_button_clicked(b):
						selected_service = tab_nest.selected_index
						service = cloud_arr[selected_service]
						accordion = accordion_arr[selected_service]
						selected_instance = accordion.selected_index
						service.toggle_instance(selected_instance)

					#terminate instance button handler
					def reboot_button_clicked(b):
						selected_service = tab_nest.selected_index
						service = cloud_arr[selected_service]
						accordion = accordion_arr[selected_service]
						selected_instance = accordion.selected_index
						service.reboot_instance(selected_instance)
						

					button.on_click(create_button_clicked)
					toggle_button.on_click(toggle_button_clicked)
					terminate_button.on_click(terminate_button_clicked)
					reboot_button.on_click(reboot_button_clicked)

				accordion = widgets.Accordion(accordion_children)

				acc_index = 0
				
				#adding titles to the accordian
				for row in instancesFormatted:
					acc_title = row['Instance Id']
					acc_title += " "
					acc_title += row['State']
					accordion.set_title(acc_index, acc_title)
					acc_index += 1
		accordion_arr.append(accordion)
		accordian_and_titles = widgets.VBox([button_and_title,accordion])
		tab_list.append(accordian_and_titles)

	tab_nest = widgets.Tab()

	tab_nest.children = tab_list
	tab_index = 0
	for service in cloud_list:
		tab_title = service.type.split(" ")
		tab_nest.set_title(tab_index, tab_title[0])
		tab_index += 1

	display(tab_nest)
	#sets global selected instance to currently selected instance
	selected_service = tab_nest.selected_index

	
