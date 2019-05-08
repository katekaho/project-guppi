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

	# initializes file from interfaces and services folders
	filenames = glob.glob('./plugins/*')
	python_files = []
	print("For useage: use %guppi help")
	f = None
	python_file = None
	for f in filenames:
		python_file = f
		python_file = python_file[10:]
		python_file = re.sub('.py', '', python_file)
		
		if python_file != '__init__' and python_file != 'pluginbase' and python_file != '_cache__':
			python_files.append(python_file)

	cloud_list = []
	cloud_index = 0
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
	@magic_arguments.magic_arguments()
	@magic_arguments.argument('arguments', nargs='*')
	def guppi(self, line=''):
		args = magic_arguments.parse_argstring(self.guppi, line)

		if(len(args.arguments) > 0):
			# ssh service
			if(args.arguments[0] == 'ssh'):
				verbose = False
				if (len(args.arguments) != 1):
					if args.arguments[1] == 'v':
						verbose = True
					#else:
					#	self.service.getInstanceInfo()
				user_interfaces.SshInterface.render_ssh_interface(self.cloud_list, self.cloud_index, verbose)
			
			
			# create instance
			elif(args.arguments[0] == 'create'):
				user_interfaces.CreateInterface.render_create_interface(self.cloud_list, self.cloud_index)
			
			# switch service
			elif(args.arguments[0] == 'switch'):
				if(len(args.arguments) < 3 and len(args.arguments) > 1):
					i = 0
					for file_name in self.python_files:
						if(args.arguments[1] == file_name):
							self.cloud_index = i
							print('set cloud interactions to '+file_name)
						i = i+1
				else:
					print("Not a valid command, type guppi switch followed by the service provider, valid services:")
					for file_name in self.python_files:
						print(file_name)

			# cloud services
			elif(args.arguments[0] == 'cloud'):
				if(len(args.arguments) < 2):
					user_interfaces.CloudInterface.render_cloud_interface(self.cloud_list, self.cloud_index)
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
