from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display
import glob
import re
import plugins
import sys

import ipywidgets as widgets
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
	for f in filenames:
		# print(f)
		python_file = f
		# print(python_file)
		python_file = python_file[10:]
		python_file = re.sub('.py', '', python_file)
		if python_file != '__init__':
			python_files.append(python_file)

	cloud_list = []
	for file_name in python_files:
		module_name = getattr(plugins, file_name)
		mod_class = getattr(module_name, file_name)
		service = mod_class()
		cloud_list.append(service)
		print("loading plugin: "+ file_name)
	print("plugins loaded")

	@line_magic
	def init(self, line):
		global service
		if(len(line) < 1):
			print("To initialize a cloud service run %init <cloud_service>")
			print("The available cloud services are:")
			
			print(self.python_files)
		else:
			found = False
			for file_name in self.python_files:
				
				if(line == file_name.lower() or line == file_name):

					module_name = getattr(plugins, file_name)
					mod_class = getattr(module_name, file_name)
					service = mod_class()
					found = True
					print("You are now using " + file_name)
					print("Re-run %guppi cloud to update")

			if(not found):
				print(line + " not found!")
				print("To see a list of available services, use %init")


	@line_magic
	@magic_arguments.magic_arguments()
	@magic_arguments.argument('arguments', nargs='*')
	def guppi(self, line=''):
		args = magic_arguments.parse_argstring(self.guppi, line)

		if(len(args.arguments) > 0):
			# cloud services
			if(args.arguments[0] == 'cloud'):
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
