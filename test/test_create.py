import unittest
import plugins

class TestCreate(unittest.TestCase):
    def test_aws_create(self):
        service = plugins.AmazonService.AmazonService()
        beforeCreate = service.get_instances_info()
        print("before create length is: " + str(len(beforeCreate)))
        service.create_instance()
        afterCreate = service.get_instances_info()
        print("after create length is: " + str(len(afterCreate)))
        self.assertTrue(len(afterCreate) == len(beforeCreate) + 1)
    
    def test_google_create(self):
        service = plugins.GoogleService.GoogleService()
        beforeCreate = service.get_instances_info()
        print("before create length is: " + str(len(beforeCreate)))
        service.create_instance()
        afterCreate = service.get_instances_info()
        print("after create length is: " + str(len(afterCreate)))
        self.assertTrue(len(afterCreate) == len(beforeCreate) + 1)
    
    def test_microsoft_create(self):
        service = plugins.MicrosoftService.MicrosoftService()
        beforeCreate = service.get_instances_info()
        print("before create length is: " + str(len(beforeCreate)))
        service.create_instance()
        afterCreate = service.get_instances_info()
        print("after create length is: " + str(len(afterCreate)))
        self.assertTrue(len(afterCreate) == len(beforeCreate) + 1)
