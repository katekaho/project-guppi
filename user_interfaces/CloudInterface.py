from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display, FileLink
import ipywidgets as widgets
import plugins

import webbrowser


selected_instance = ""
accordion_arr =""
tab_nest = ""
cloud_arr = ""

service = ""

#===================================================#
#-----------------Button-Functions------------------#
#===================================================#
def create_button_clicked(b):
	global selected_service
	global tab_nest
	global cloud_arr

	selected_service = tab_nest.selected_index

	service = cloud_arr[selected_service]
	service.create_instance()

def button1Clicked(b):
	webbrowser.open_new_tab('https://console.cloud.google.com/')
def button2Clicked(b):
	webbrowser.open_new_tab('https://console.cloud.google.com/cloud-resource-manager')
def button3Clicked(b):
	webbrowser.open_new_tab('https://cloud.google.com/billing/docs/how-to/modify-project')
def button4Clicked(b):
	webbrowser.open_new_tab('https://cloud.google.com/sdk/')
def button6Clicked(b):
	webbrowser.open_new_tab('https://cloud.google.com/apis/docs/enable-disable-apis?hl=en&ref_topic=6262490&visit_id=636909616876722358-4171110160&rd=1')
def button7Clicked(b):
	webbrowser.open_new_tab('https://cloud.google.com/storage/docs/creating-buckets')
def button8Clicked(b):
	webbrowser.open_new_tab('https://console.cloud.google.com/projectselector/apis/credentials/serviceaccountkey?supportedpurview=project')
def button9Clicked(b):
	webbrowser.open_new_tab('https://console.cloud.google.com/projectselector/apis/credentials/serviceaccountkey?supportedpurview=project')


#terminate instance button handler
def terminate_button_clicked(b):
	global selected_instance
	global accordion_arr
	global service
	global selected_service
	global tab_nest
	global cloud_arr
	selected_service = tab_nest.selected_index

	service = cloud_arr[selected_service]
	accordion = accordion_arr[selected_service]
	selected_instance = accordion.selected_index
	service.terminate_instance(selected_instance)


#toggle instance button handler
def toggle_button_clicked(b):
	global selected_instance
	global accordion_arr
	global service
	global selected_service
	global tab_nest
	global cloud_arr

	selected_service = tab_nest.selected_index

	service = cloud_arr[selected_service]
	accordion = accordion_arr[selected_service]
	
	selected_instance = accordion.selected_index
	service.toggle_instance(selected_instance)


#terminate instance button handler
def reboot_button_clicked(b):
	global selected_instance
	global accordion_arr
	global selected_service
	global tab_nest
	global service
	global cloud_arr

	selected_service = tab_nest.selected_index

	service = cloud_arr[selected_service]
	accordion = accordion_arr[selected_service]
	selected_instance = accordion.selected_index

	service.reboot_instance(selected_instance)

#===================================================#
#------------Cloud-Interface-Function---------------#
#===================================================#
def render_cloud_interface(cloud_list):
	global selected_instance
	global accordion_arr
	global service
	global selected_service
	global tab_nest
	global cloud_arr

	cloud_arr = cloud_list
	tab_list = []
	accordion_arr = []

	for cloud_service in cloud_list:
		service = cloud_service

		type_label = widgets.HTML(value="<b>"+service.type+"<b>")

		if(service.check_setup() == False):
			# Change later to be dynamic

			
			accordion = widgets.Accordion([])
			fn = "./"+service.name +"Setup.txt"
			html_as_str = open(fn, 'r').read()
			setup = widgets.HTML(value=html_as_str)

			button_and_title = widgets.VBox([setup])
			
			# if(service.type == "AWS SERVICE"):
			# 	display(HTML(filename="./AmazonSetup.html"))
			# if(service.type == "GOOGLE SERVICE"):
			# 	print('False')
			# 	accordion = widgets.Accordion([])
			# 	info =  widgets.HTML(value="Setup Instructions")
			# 	text1 = widgets.HTML(value="Create a Google Cloud account or sign onto your existing one")
			# 	button1 = widgets.Button(description="Go to Google cloud")
			# 	button1.on_click(button1Clicked)
				
			# 	text2 = widgets.HTML(value="Select or create a Google Cloud Platform project")
			# 	button2 = widgets.Button(description="Go to manage resources page")
			# 	button2.on_click(button2Clicked)

			# 	text3 = widgets.HTML(value="Make sure that billing is enabled for your Google Cloud Platform Project")
			# 	button3 = widgets.Button(description="Learn How to enable billing")
			# 	button3.on_click(button3Clicked)

			# 	text4 = widgets.HTML(value="Install the Cloud SDK")
			# 	button4 = widgets.Button(description="Go to installation page")
			# 	button4.on_click(button4Clicked)

			# 	text5 = widgets.HTML(value="Go to your command line and 'run gcloud auth application-default login'")

			# 	text6 = widgets.HTML(value="Install the google-api-python-client library: pip install --upgrade google-api-python-client")
			# 	button6 = widgets.Button(description="View google api page")
			# 	button6.on_click(button6Clicked)

			# 	text7 = widgets.HTML(value="Enable the Google Cloud Storage API and Cloud Resource Manager API")
			# 	button7 = widgets.Button(description="View instructions")
			# 	button7.on_click(button7Clicked)

			# 	text8 = widgets.HTML(value="Create a storage bucket and note the bucket name for later")
			# 	button8 = widgets.Button(description="View instructions")
			# 	button8.on_click(button8Clicked)

			# 	text9 = widgets.HTML(value="Create a service account for authentication")
			# 	button9 = widgets.Button(description="Go to admin page")
			# 	button9.on_click(button9Clicked)

			# 	text10 = widgets.HTML(value="From the Service account list, select New service account.")
			# 	text11 = widgets.HTML(value="In the Service account name field, enter a name.")
			# 	text12 = widgets.HTML(value="From the Role list, select Project > Owner.")
			# 	text13 = widgets.HTML(value="Click Create. This should download a JSON key")
			# 	text14 = widgets.HTML(value="Move this key file into the googleCredentials folder found in guppi/plugins")
			# 	text15 = widgets.HTML(value="Reload the'guppi cloud' command")

			# 	array = [info, type_label,text1,button1, text2, button2, text3, button3, text4, button4, text5, text6, button6, text7, button7, text8, button8, text9, button9, text10, text11, text12, text13, text14, text15]

			# 	button_and_title = widgets.VBox(array)
		else:
			instancesFormatted = service.get_instances_info()
			# display(type_label)
			button = widgets.Button(description="Create Instance")
			# display(button)
			button.on_click(create_button_clicked)
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
	selected_instance = accordion.selected_index
	selected_service = tab_nest.selected_index