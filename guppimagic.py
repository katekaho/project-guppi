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
service = plugins.AmazonService.AmazonService()

@magics_class
class GuppiMagic(Magics):
	filenames = glob.glob('./plugins/*.py')
	python_files = []
	for f in filenames:
		python_file = re.sub('./plugins\\\\', '', f)
		python_file = re.sub('.py', '', python_file)
		if python_file != '__init__':
			python_files.append(python_file)
	
	print(python_files)

	@line_magic
	def init(self, line):
		global service
		print(self.python_files)
		found = False
		for file_name in self.python_files:
			
			if(line == file_name.lower()):

				module_name = getattr(plugins, file_name)
				mod_class = getattr(module_name, file_name)
				service = mod_class()
				found = True
				print("You are now using " + file_name)
				print("Re-run %db to update")

		if(not found):
			print(line + " not found!")

	@line_magic
	@magic_arguments.magic_arguments()
	@magic_arguments.argument('arguments', nargs='*')
	def guppi(self, line=''):
		args = magic_arguments.parse_argstring(self.guppi, line)

		if(len(args.arguments) > 0):
			# cloud services
			if(args.arguments[0] == 'cloud'):
				user_interfaces.CloudInterface.render_cloud_interface(service)
			#slack service
			elif(args.arguments[0] == 'slack'):
				if(len(args.arguments)>1):
					if(args.arguments[1] == 'view'):
						user_interfaces.SlackInterface.render_slack_interface()
					elif(args.arguments[1] == 'send'):
						if(len(args.arguments)< 2):
							print("Please enter a channel name: %guppi slack send [channel_name] [\"MESSAGE\"]")
						else:
							if(len(args.arguments)< 4):
								print("Please enter a message: %guppi slack send [channel_name] [\"MESSAGE\"]")
								print("Note: message must be in quotes")
							elif(len(args.arguments)> 4):
								print("Your message must be in quotes")
							else:
								user_interfaces.SlackInterface.send_message(args.arguments[2],args.arguments[3])
				else:
					print("For usage, use the %guppi help command")
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
