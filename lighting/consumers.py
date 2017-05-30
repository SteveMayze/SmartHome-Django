
from channels.generic.websockets import WebsocketDemultiplexer
from lighting.models import LightingStateBinding

class Demultiplexer(WebsocketDemultiplexer):        
        consumers = {
                "tl2c_state": LightingStateBinding.consumer,
        }

        groups = ["binding.tl2c",]
