from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display

from amazonregister import AmazonService
from googleregister import GoogleService
from microsoftregister import MicrosoftService

import ipywidgets as widgets

# TODO fix switching instances with init, needs to clear accordian
selected_instance = ""
accordion =""
service = AmazonService()


#create instance button handler
def create_button_clicked(b):
	
	service.create_instance()

#terminate instance button handler
def terminate_button_clicked(b):
	global selected_instance
	global accordion
	selected_instance = accordion.selected_index

	service.terminate_instance(selected_instance)


#toggle instance button handler
def toggle_button_clicked(b):
	global selected_instance
	global accordion
	selected_instance = accordion.selected_index

	service.toggle_instance(selected_instance)


#terminate instance button handler
def reboot_button_clicked(b):
	global selected_instance
	global accordion
	selected_instance = accordion.selected_index

	service.reboot_instance(selected_instance)

@magics_class
class TestMagics(Magics):
	@line_magic
	def init(self, line):
		global service
		if(line == "aws"):
			service = AmazonService()
			print("You are now using AWS")
		elif(line == "google"):
			service = GoogleService()
			print("You are now using Google")
		elif(line == "microsoft"):
			service = MicrosoftService()
			print("You are now using Microsoft")
		print("Re-run %db to update")
	@line_magic
	def db(self, line):
		global selected_instance
		global accordion

		instancesFormatted = service.get_instances_info()
		
		type_label = widgets.HTML(value="<b>"+service.type+"<b>")
		display(type_label)
		button = widgets.Button(description="Create Instance")
		display(button)
		button.on_click(create_button_clicked)

		#stores the info and buttons for each instance
		accordion_children = []
		if (len(instancesFormatted) == 0):
			print("No instances found, press 'Create Instance' to create one")
		else:
			for row in instancesFormatted:
				#appends all info into array of labels
				info = ["<b>Instance Type:</b>", row['Instance Type'] ,"<b>Availability Zone:</b>", row['Availability Zone'], "<b>State:<b>" , row['State']]

				#makes each label html and puts into HBox
				items = [widgets.HTML(str(i)) for i in info]
				instance_info = widgets.HBox(items)

				#buttons

				# To-do: decide and generalize state names so this looks clean
				
				if(row['State'] == "running" or row['State'] == "RUNNING"): 
					toggle_button = widgets.Button(description='Stop Instance')
				elif(row['State'] == "stopped" or row['State'] == 'TERMINATED'):
					toggle_button = widgets.Button(description='Start Instance')
				else:
					toggle_button = widgets.Button(description='Start Instance',disabled=True)

				#disables the terminate button when not running or stopped
				if(row['State'] == "running" or row['State'] == "stopped"
					or row['State'] == "RUNNING" or row['State'] == 'TERMINATED'):
					terminate_button = widgets.Button(description='Terminate Instance')
				else:
					terminate_button = widgets.Button(description='Terminate Instance',disabled=True)
				# reboot button
				if(row['State'] == "running" or row['State'] == "RUNNING"):
					reboot_button = widgets.Button(description='Reboot Instance')
				else:
					reboot_button = widgets.Button(description='Reboot Instance',disabled=True)


				file = open("icons/running.png", "rb")

				if(row['State'] == "running" or row['State'] == "RUNNING"):
					file = open("icons/running.png", "rb")
				elif(row['State'] == "pending"or row['State'] == 'STAGING'):
					file = open("icons/pending.png", "rb")
				elif(row['State'] == "stopping" or row['State'] == 'STOPPING'):
					file = open("icons/stopping.png", "rb")
				elif(row['State'] == "stopped"or row['State'] == 'TERMINATED'):
					file = open("icons/stopped.png", "rb")
				elif(row['State'] == "shutting-down"):
					file = open("icons/shutting-down.png", "rb")
				else:
					file = open("icons/terminated.png", "rb")

				image = file.read()
				indicator = widgets.Image(value=image,format='png')
				

				toggle_button.on_click(toggle_button_clicked)
				terminate_button.on_click(terminate_button_clicked)
				reboot_button.on_click(reboot_button_clicked)

				buttons = [toggle_button,reboot_button,terminate_button,indicator]
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
