###############################################################################
#                            RUN MAIN                                         #
###############################################################################

from instance.config.app_settings import *
from instance.config.file_system import *
from application.server import server

app = server.app(name=name)

app.run()

#http://localhost:5000/data?symbol=UCG.MI&from=2019-06-01&to=2019-08-31&variable=Close
