
from channels.generic.websockets import WebsocketDemultiplexer
from lighting.models import LightHistoryBinding

class Demultiplexer(WebsocketDemultiplexer):        
        consumers = {
                "tl2c_state": LightHistoryBinding.consumer,
        }

        groups = ["binding.tl2c",]
