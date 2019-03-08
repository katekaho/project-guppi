import unittest
import plugins

class TestTerminate(unittest.TestCase):
    def setUp(self):
        # set index to index to be deleted or -1 to delete the most recent instance
        self.index = -1

    def test_aws_terminate(self):
        # set service to Amazon
        service = plugins.AmazonService.AmazonService()
        beforeTerminate = service.get_instances_info()
        # set index to the most recent instance if self.index == -1
        index = self.index
        if(index < 1):
            index = len(beforeTerminate) - 1
        print('before terminate length is: ' + str(len(beforeTerminate)))
        service.terminate_instance(self.index)
        afterTerminate = service.get_instances_info()
        if(len(beforeTerminate) == 0):
            print('Amazon: nothing to terminate')
            self.assertTrue(True)        
        elif(len(afterTerminate) == len(beforeTerminate) - 1):
            self.assertTrue(True)
        elif(afterTerminate[self.index]['State'] == 'shutting-down'):
            self.assertTrue(True)
        elif(afterTerminate[self.index]['State'] == 'terminated'):
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_google_terminate(self):
        # set service to Google
        service = plugins.GoogleService.GoogleService()
        beforeTerminate = service.get_instances_info()
        # set index to the most recent instance if self.index == -1
        index = self.index
        if(index < 1):
            index = len(beforeTerminate) - 1
        print('before terminate length is: ' + str(len(beforeTerminate)))
        service.terminate_instance(self.index)
        afterTerminate = service.get_instances_info()
        if(len(beforeTerminate) == 0):
            print('Google: nothing to terminate')
            self.assertTrue(True)        
        elif(len(afterTerminate) == len(beforeTerminate) - 1):
            self.assertTrue(True)
        elif(afterTerminate[self.index]['State'] == 'STOPPING'):
            self.assertTrue(True)
        elif(afterTerminate[self.index]['State'] == 'TERMINATED'):
            self.assertTrue(True)

    def test_microsoft_terminate(self):
        # set service to Microsoft
        service = plugins.MicrosoftService.MicrosoftService()
        beforeTerminate = service.get_instances_info()
        # set index to the most recent instance if self.index == -1
        index = self.index
        if(index < 1):
            index = len(beforeTerminate) - 1
        print('before terminate length is: ' + str(len(beforeTerminate)))
        service.terminate_instance(self.index)
        afterTerminate = service.get_instances_info()
        if(len(beforeTerminate) == 0):
            print('Microsoft: nothing to terminate')
            self.assertTrue(True)
        elif(len(afterTerminate) == len(beforeTerminate) - 1):
            self.assertTrue(True)
        elif(afterTerminate[self.index]['State'] == 'Deleting'):
            self.assertTrue(True)