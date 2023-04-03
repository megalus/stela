from controllers import HelloWorldController
from starlite import Starlite

app = Starlite(route_handlers=[HelloWorldController])
