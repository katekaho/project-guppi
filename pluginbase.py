from abc import ABC, abstractmethod

class PluginBase(ABC):   
  @abstractmethod
  def get_instances_info(self):
    pass
  
  @abstractmethod
  def create_instance(self):
    pass
  
  @abstractmethod
  def terminate_instance(self, instance):
    pass

  @abstractmethod
  def toggle_instance(self, instance):
    pass