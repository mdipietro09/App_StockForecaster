###############################################################################
#                            RUN MAIN                                         #
###############################################################################

from instance.config.app_settings import *
from instance.config.file_system import *
from app.server import server



app = server.create_app(name=name)

app.run(host=host, port=port, threaded=threaded, debug=debug)

#http://localhost:5000/data?symbol=UCG.MI&from=2019-06-01&to=2019-08-31&variable=Close
