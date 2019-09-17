###############################################################################
#                                MAIN                                         #
###############################################################################

import logging
import flask

from model.data import data
from instance.config.file_system import *



'''
'''
def create_app(name=None, host="0.0.0.0", port="80", threaded=False, debug=False):
    ## app object
    name = name if name is not None else __name__
    app = flask.Flask(name, instance_relative_config=True, 
                      template_folder=dirpath+'app/client/templates',
                      static_folder=dirpath+'app/client/static')
    
        
    ## config   
    #app.config.from_pyfile("dirpath+instance.config.app_settings.py", silent=True)
    
    
    ## api
    @app.route('/ping', methods=["GET"])
    def ping():
        return 'pong'
    
    @app.route("/", methods=["GET"])
    def index():
        #return flask.send_from_directory(directory=config.dirpath+"app/templates/", filename="index.html")
        return flask.render_template("index.html")
    
    @app.route("/data", methods=['GET', 'POST'])
    def get_data():
        try:
            if flask.request.method == 'POST':
                ### input dal client
                #symbol = flask.request.args["symbol"]
                #from_str = flask.request.args["from"]
                #to_str = flask.request.args["to"]
                #variable = flask.request.args["variable"]
                symbol = flask.request.form["symbol"]
                from_str = flask.request.form["from"]
                to_str = flask.request.form["to"]
                variable = flask.request.form["variable"]
                ### get data
                stock = data(symbol, from_str, to_str, variable)
                stock.get_dates()
                stock.get_data()
                img = stock.plot_ts(plot_ma=True, plot_intervals=True, window=30, figsize=(20,13))
                #return flask.send_file(img, attachment_filename='plot.png', mimetype='image/png')
                return flask.render_template("data.html", img=img)
            else:
                return flask.render_template("data.html")
        except Exception as e:
            flask.abort(500)
    
    
    ## errors
    @app.errorhandler(404)
    def page_not_found(e):
        return flask.render_template("errors.html", msg="Page doesn't exist"), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return flask.render_template('errors.html', msg="Something went terribly wrong"), 500
    
    
    return app