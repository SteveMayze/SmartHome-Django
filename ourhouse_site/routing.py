

from channels import route_class, route
from main.consumers import Demultiplexer

channel_routing = [
	route_class(Demultiplexer, path="^/stream/?$"),
]


