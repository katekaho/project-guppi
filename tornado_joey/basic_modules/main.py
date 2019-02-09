#!/usr/bin/env python
import os.path
import boto3    

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
      (r"/", MainHandler),
      (r"/create", CreateInstanceHandler),
      (r"/end", EndInstanceHandler),
      (r"/terminate", TerminateInstanceHandler),
    ]
    settings = dict(
      template_path=os.path.join(os.path.dirname(__file__), "templates"),
      static_path=os.path.join(os.path.dirname(__file__), "static"),
      ui_modules={"Instance": InstanceModule},
      debug=True,
      autoescape=None
      )
    tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.render(
      "index.html",
      instanceList=getInstanceInfo(),
    )

class CreateInstanceHandler(tornado.web.RequestHandler):
  def post(self):
    ec2 = boto3.resource('ec2')

    ec2.create_instances(
      ImageId='ami-0cd3dfa4e37921605',
      MinCount=1,
      MaxCount=1,
      InstanceType='t2.micro',
      KeyName='ec2-keypair1',
    )
    self.redirect('/')

class EndInstanceHandler(tornado.web.RequestHandler):
  def post(self):
    ec2 = boto3.resource('ec2')
    instanceId = self.get_argument('stopInstanceId')
    print(instanceId)
    ids = [instanceId]
    ec2.instances.filter(InstanceIds=ids).stop()
    self.redirect('/')

class TerminateInstanceHandler(tornado.web.RequestHandler):
  def post(self):
    ec2 = boto3.resource('ec2')
    instanceId = self.get_argument('terminateInstanceId')
    print(instanceId)
    ids = [instanceId]
    ec2.instances.filter(InstanceIds=ids).terminate()
    self.redirect('/')

class InstanceModule(tornado.web.UIModule):
  def render(self, instance):
    return self.render_string(
      "modules/instance.html", 
      instance=instance
    )
    
  def css_files(self):
    return "css/instance.css"

  #Code for running javascript file
  # def javascript_files(self):
  # 	return "js/sample.js"

def main():
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  print('Server listening on http://localhost:' + str(options.port))
  tornado.ioloop.IOLoop.instance().start()

def getInstanceInfo():
  ec2client = boto3.client('ec2')
  response = ec2client.describe_instances()

  reservations = response.get('Reservations')
  instances = []

  for reservation in reservations:
    reservationInstances = reservation.get('Instances')
    for inst in reservationInstances:
      instances.append(inst)
  
  instancesFormatted = []

  for instance in instances:
    tags = instance.get('Tags', [])
    name = ''
    for tag in tags:
      tagKey = tag.get('Key', '')
      if tagKey == 'Name':
        name = tag['Value']

    placement = instance['Placement']
    availabilityZone = placement['AvailabilityZone']

    state = instance['State']
    stateName = state.get('Name', '')

    launchTime = instance.get('LaunchTime', '')

    if len(name) > 20:
      name = name[:20] + '...'

    formatInst = {
      'Name': name,
      'InstanceId': instance.get('InstanceId', ''),
      'InstanceType': instance.get('InstanceType', ''),
      'AvailabilityZone': availabilityZone,
      'State': stateName,
      'KeyName': instance.get('KeyName', ''),
      'LaunchTime': launchTime,
    }
    instancesFormatted.append(formatInst)
  
  return instancesFormatted

if __name__ == "__main__":
  main()
