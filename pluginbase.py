from abc import ABC, abstractmethod

class PluginBase(ABC):  
	@abstractmethod
	def create_instance(self):
		pass
  
	@abstractmethod
	def get_instances_info(self):
		pass
  
	@abstractmethod
	def terminate_instance(self, instance):
		pass

	@abstractmethod
	def toggle_instance(self, instance):
		pass

	@abstractmethod
	def reboot_instance(self, instance):
		pass