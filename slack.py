from slackclient import SlackClient
import os


token = "xoxp-524358460228-524727397301-562934358338-57f264d9e922b399e56952c65bac020f"
sc = SlackClient(token)


# sends a new message to passed in channel_name and message
def post_message(channel_name, message):
	sc.api_call(
		"chat.postMessage",
		channel=channel_name,
		text=message,
	)


def get_username(user_id):
	users_list = sc.api_call("users.list")
	for member in users_list['members']:
		if(member['id'] == user_id):
			return member['name']

def get_channel_id(channel_name):
	channels_list = sc.api_call("channels.list")
	for channel in channels_list['channels']:
		if(channel['name']== channel_name):
			return channel['id']
	return channel_name + "does not exist"

def get_latest_messages(channel_name):
	channel_id = get_channel_id(channel_name)
	message_list = sc.api_call(
					"channels.history",
					channel=channel_id,
					count = 5,
					)
	for message in message_list['messages']:
		if('user' in message):
			name = get_username(message['user'])
			message['user'] = name

	return message_list['messages']


print(get_latest_messages("backend"))