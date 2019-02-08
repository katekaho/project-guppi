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
			instanceList=getInfo()	
		)


class InstanceModule(tornado.web.UIModule):
	def render(self, instance):
		return self.render_string(
			"modules/instance.html", 
			instance=instance
		)

	# def html_body(self):
	# 	return "<div class=\"addition\"><p>html_body()</p></div>"
	
	# def embedded_javascript(self):
	# 	return "document.write(\"<p>embedded_javascript()</p>\")"
	
	# def embedded_css(self):
	# 	return ".addition {color: #FF00FF}"
		
	def css_files(self):
		return "css/instance.css"
	
	# def javascript_files(self):
	# 	return "js/sample.js"

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
	# getInfo()
	

def getInfo():
	ec2client = boto3.client('ec2')
	response = ec2client.describe_instances()
	return response
	# for reservation in response["Reservations"]:
	# 	for instance in reservation["Instances"]:
	# 		# This sample print will output entire Dictionary object
	# 		print(instance)
			
	# 		# This will print will output the value of the Dictionary key 'InstanceId'
	# 		print(instance["InstanceId"])

	# 		print("")
	# 		print("")

if __name__ == "__main__":
	main()
