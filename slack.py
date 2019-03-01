from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display

import ipywidgets as widgets
from ipywidgets import Layout, Button, Box, FloatText, Textarea, Dropdown, Label, IntSlider
from datetime import datetime

from slackclient import SlackClient
import os
import sys

token = "xoxp-524358460228-524727397301-562934358338-57f264d9e922b399e56952c65bac020f"
sc = SlackClient(token)

#===================================================
#---------------Slack-API-Funtions------------------
#===================================================

# returns dict with user info
def user_info():
	users_list = sc.api_call("users.list")
	users = []
	for member in users_list['members']:
		profile = member['profile']
		user = {
			'id': member.get('id',''),
			'username': member.get('name',''),
			'real_name': profile.get('real_name_normalized','')
		}
		users.append(user)
	return users
		
# sends a new message to passed in channel_name and message
def post_message(channel_name, message):
	result = sc.api_call(
		"chat.postMessage",
		channel=channel_name,
		text=message,
	)
	if(result.get('ok','') == True):
		print("Message sent to " +channel_name)
	else:
		print('Message could not be sent')
		print(result.get('error',''))

#pass in userid, returns associated username
def get_username(user_id, users):
	for user in users:
		if(user_id == user.get('id','')):
			return user.get('real_name','')
	return "no username"

#pass in channel name, returns associated channel id
def get_channel_id(channel_name):
	channels_list = sc.api_call("channels.list")
	for channel in channels_list['channels']:
		if(channel['name']== channel_name):
			return channel['id']
	return channel_name + "does not exist"

#pass in channel_name and number of messages, returns last x messages from channel
def get_latest_messages(channel_name, users, num_messages):
	channel_id = get_channel_id(channel_name)
	message_list = sc.api_call(
					"channels.history",
					channel=channel_id,
					count = num_messages,
					)
	#replaces userid with users actual name
	for message in message_list['messages']:
		if('user' in message):
			name = get_username(message['user'],users)
			message['user'] = name
	return message_list['messages']

#===================================================
#---------------Slack-Magic-Class-------------------
#===================================================

@magics_class
class SlackMagic(Magics):
	channel_name = ""
	message = ""
	
	#takes in channel name, outputs last x messages
	def display_messages(self,channel):
		users = user_info()
		self.channel_name = channel

		# gets last 10 messages
		messages = get_latest_messages(channel,users,10)

		for message in reversed(messages):
			if('user' in message):
				username = widgets.HTML(value="<b>"+message['user']+":<b>",layout=Layout(width='25%'))
			elif('username' in message):
				username = widgets.HTML(value="<b>"+message['username']+":<b>",layout=Layout(width='25%'))

			message_content = widgets.HTML(value= message['text'],layout=Layout(width='70%'))

			ts = float(message['ts'])
			formatted_time = datetime.utcfromtimestamp(ts).strftime('%H:%M')
			empty_space = widgets.HTML(value= '',layout=Layout(width='5%'))
			timestamp = widgets.HTML(value= formatted_time)

			box_layout = Layout(
				border='solid 1px',
				padding='1em',
				width= '100%',
			)
			message_box = Box([username,message_content,empty_space,timestamp], layout=box_layout)

			display(message_box)

	#takes in channel name and message, sends message to channel
	def send_message(self,channel,message):
			post_message(channel, message)

	#takes in jupyter inputs 
	@line_magic
	@magic_arguments.magic_arguments()
	@magic_arguments.argument('arguments', nargs='*')
	def slack(self, line=''):
		args = magic_arguments.parse_argstring(self.slack, line)
		if(len(args.arguments) > 0):
			if(args.arguments[0] == 'help'):
				print("View a slack channel:\n%slack view [channel_name]\n\nSend a Slack message: \n%slack send [channel_name] [message in quotes]")
			elif(args.arguments[0] == 'view'):
				if(len(args.arguments)< 2):
					print("Please enter a channel name: %slack [view] [channel_name]")
				else:
					self.display_messages(args.arguments[1])
			elif(args.arguments[0] == 'send'):
				if(len(args.arguments)< 2):
					print("Please enter a channel name: %slack [send] [channel_name] [\"MESSAGE\"]")
				else:
					if(len(args.arguments)< 3):
						print("Please enter a message: %slack [send] [channel_name] [\"MESSAGE\"]")
						print("Note: message must be in quotes")
					elif(len(args.arguments)> 3):
						print("Your message must be in quotes")
					else:
						self.send_message(args.arguments[1],args.arguments[2])
		else:
			print("For usage, use the  %slack help command")

#===================================================
#-----------ipython-Magic-Registering---------------
#===================================================

def load_ipython_extension(ipython):
	"""This function is called when the extension is
	loaded. It accepts an IPython InteractiveShell
	instance. We can register the magic with the
	`register_magic_function` method of the shell
	instance."""
	ipython.register_magics(SlackMagic)