import unittest
import plugins

class TestGetInstanceInfo(unittest.TestCase):
    def setUp(self):
        self.index = 0

    def test_aws_terminate(self):
        service = plugins.AmazonService.AmazonService()
        beforeTerminate = service.get_instances_info()
        print('before terminate length is: ' + str(len(beforeTerminate)))
        service.terminate_instance(self.index)
        afterTerminate = service.get_instances_info()
        if(len(beforeTerminate) == len(afterTerminate) + 1):
            self.assertTrue(True)
        elif(afterTerminate[self.index]['State'] == 'shutting-down'):
            self.assertTrue(True)
        elif(afterTerminate[self.index]['State'] == 'terminated'):
            self.assertTrue(True)
        else:
            self.assertTrue(False)