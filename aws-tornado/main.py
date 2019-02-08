import os.path
import random
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import boto3
from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', instanceInfo=self.getInstanceInfo())
    def post(self):
        ec2 = boto3.resource('ec2')
        # create a new EC2 instance
        instances = ec2.create_instances(
            ImageId='ami-0cd3dfa4e37921605',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName='ec2-keypair1'
        )
        self.render('index.html', instanceInfo=self.getInstanceInfo())
    def getInstanceInfo(self):
        ec2client = boto3.client('ec2')
        response = ec2client.describe_instances()
        instanceList = []
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                # This sample print will output entire Dictionary object
                instanceList.append(instance["InstanceId"])
        return instanceList

class MungedPageHandler(tornado.web.RequestHandler):
    def map_by_first_letter(self, text):
        mapped = dict()
        for line in text.split('\r\n'):
            for word in [x for x in line.split(' ') if len(x) > 0]:
                if word[0] not in mapped: mapped[word[0]] = []
                mapped[word[0]].append(word)
        return mapped
    

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
    handlers=[(r'/', IndexHandler), (r'/poem', MungedPageHandler)],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()