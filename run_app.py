###############################################################################
#                            RUN MAIN                                         #
###############################################################################

from instance import config
from app.server import server

server.app(name=config.name, host=config.host, port=config.port, threaded=config.threaded, debug=config.debug)

#http://localhost:5000/data?symbol=UCG.MI&from=2019-06-01&to=2019-08-31&variable=Close
