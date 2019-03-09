import unittest
import plugins
import user_interfaces.SlackInterface as slack

class TestSlack(unittest.TestCase):
    def setUp(self):
        self.channel_name = 'random'
        self.message = 'sent from unit test again'
        self.users = slack.user_info()
    
    def test_post_get_latest(self):
        slack.post_message(self.channel_name, self.message)
        messages = slack.get_latest_messages(self.channel_name, self.users, 3)
        success = False
        for message in messages:
            if message['text'] == self.message:
                success = True
        self.assertTrue(success)