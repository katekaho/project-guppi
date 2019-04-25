from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display
import glob
import re
import plugins
import sys
import paramiko

import ipywidgets as widgets
from ipywidgets import Layout, Button, Box, FloatText, Textarea, Dropdown, Label, IntSlider
import user_interfaces

selected_instance = ""
accordion =""

# Setting default service
service = ""

@magics_class
class GuppiMagic(Magics):
	filenames = glob.glob('./plugins/*.py')
	python_files = []
	print("For useage: use %guppi help")
	f = None
	python_file = None
	for f in filenames:
		# print(f)
		python_file = f
		# print(python_file)
		python_file = python_file[10:]
		python_file = re.sub('.py', '', python_file)
		if python_file != '__init__':
			python_files.append(python_file)

	cloud_list = []
	file_name = None
	module_name = None
	mod_class = None
	for file_name in python_files:
		module_name = getattr(plugins, file_name)
		mod_class = getattr(module_name, file_name)
		service = mod_class()
		cloud_list.append(service)
		print("loading plugin: "+ file_name)
	print("plugins loaded")

	
	@line_magic
	def ssh(self, line):
		instances = self.cloud_list[0].get_instances_info()
		box_list = []	
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

				box_list.append(cb)
		boxes_container = widgets.VBox(box_list)

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

		# button clicked function
		def submit_button_clicked(b):
			for checkbox in box_list:
				if(checkbox.value == True):
					print("---------------------------------------------------")
					print(checkbox.description)
					print("---------------------------------------------------")
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

		submit_button.on_click(submit_button_clicked)


	@line_magic
	@magic_arguments.magic_arguments()
	@magic_arguments.argument('arguments', nargs='*')
	def guppi(self, line=''):
		args = magic_arguments.parse_argstring(self.guppi, line)

		if(len(args.arguments) > 0):

			if(args.arguments[0] == 'ssh'):
				user_interfaces.SshInterface.render_ssh_interface(self.cloud_list)

			# cloud services
			elif(args.arguments[0] == 'cloud'):
				if(len(args.arguments) < 2):
					user_interfaces.CloudInterface.render_cloud_interface(self.cloud_list)
				else:
					print(args.arguments[1] +" is not a cloud command, for usage, use %guppi help")
				
			#slack service
			elif(args.arguments[0] == 'slack'):
				if(len(args.arguments)>1):
					if(args.arguments[1] == 'view'):
						if(len(args.arguments)< 3):
							user_interfaces.SlackInterface.render_slack_interface()
						else:
							print(args.arguments[2] +" is not a slack command, for usage, use %guppi help")
					elif(args.arguments[1] == 'send'):
						if(len(args.arguments)< 2):
							print("Please enter a channel name: %guppi slack send <channel_name> <\"MESSAGE\">")
						else:
							if(len(args.arguments)< 4):
								print("Please enter a message: %guppi slack send <channel_name> <\"MESSAGE\">")
								print("Note: message must be in quotes")
							elif(len(args.arguments)> 4):
								print("Your message must be in quotes")
							else:
								user_interfaces.SlackInterface.send_message(args.arguments[2],args.arguments[3])
					else:
						print(args.arguments[1] +" is not a slack command, for usage, use %guppi help")
				else:
					print("For Slack usage, use %guppi help ")

			# github service
			elif(args.arguments[0] == 'github'):
				if(len(args.arguments) < 2):
					user_interfaces.GitHubInterface.display_notifications(5)
				else:
					try:
						num = int(args.arguments[1])
					except ValueError:
						print("Number of notifications must be an integer")
					else:
						user_interfaces.GitHubInterface.display_notifications(num+1)
			elif(args.arguments[0] == 'help'):
				print("To see a list of available cloud services, use:\n%init\n")
				print("To choose a cloud service to view, use:\n%init <cloud_service>\n")
				print("To view a cloud service, use:\n%guppi cloud\n")
				print("To view Slack messages, use:\n%guppi slack view\n")
				print("To send a Slack message, use:\n%guppi slack send <channel_name> <message in quotes>\n")
				print("To view GitHub notifications, use:\n%guppi github <number_of_notifications>\n")
			else:
				print(args.arguments[0] + " is not a guppi command, for usage, use %guppi help")
					
		else:
			print("For usage, use the %guppi help command")


#===================================================#
#-----------ipython-Magic-Registering---------------#
#===================================================#

def load_ipython_extension(ipython):
	"""This function is called when the extension is
	loaded. It accepts an IPython InteractiveShell
	instance. We can register the magic with the
	`register_magic_function` method of the shell
	instance."""
	ipython.register_magics(GuppiMagic)
