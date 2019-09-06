###############################################################################
#                            RUN MAIN                                         #
###############################################################################

from instance.config.appsettings import *
from instance.config.filesystem import *
from app.server import server

server.app(name=name, host=host, port=port, threaded=threaded, debug=debug)

#http://localhost:5000/data?symbol=UCG.MI&from=2019-06-01&to=2019-08-31&variable=Close
