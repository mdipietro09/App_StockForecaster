###############################################################################
#                                MAIN                                         #
###############################################################################

import flask
from tensorflow.keras import models
import pandas as pd
import ast

from model.data import data
from model.lstm import lstm
from instance.config.file_system import *



'''
'''
def create_app(name=None):
    ## app object
    name = name if name is not None else __name__
    app = flask.Flask(name, instance_relative_config=True, 
                      template_folder=dirpath+'app/client/templates',
                      static_folder=dirpath+'app/client/static')
    
    
    ## api
    @app.route('/ping', methods=["GET"])
    def ping():
        return 'pong'
    
    
    @app.route("/", methods=['GET', 'POST'])
    def index():
        try:
            if flask.request.method == 'POST':
                ### input dal client
                symbol = flask.request.form["symbol"]
                from_str = flask.request.form["from"]
                to_str = flask.request.form["to"]
                variable = flask.request.form["variable"]
                parameters = {"symbol":symbol, "from_str":from_str, "to_str":to_str, "variable":variable}
                app.logger.info(parameters)
                ### redirect
                app.logger.info("Redirecting...") 
                return flask.redirect(flask.url_for("forecaster", parameters=str(parameters)))
            else:
                return flask.render_template("index.html")
        except Exception as e:
            app.logger.error(e)
            flask.abort(500)
    
    
    @app.route("/forecaster/<parameters>", methods=['GET', 'POST'])
    def forecaster(parameters):
        try:
            ### get data
            app.logger.info("...Redirected")
            parameters = ast.literal_eval(parameters)
            symbol = parameters["symbol"]
            from_str = parameters["from_str"]
            to_str = parameters["to_str"]
            variable = parameters["variable"]
            stock = data(symbol, from_str, to_str, variable)
            stock.get_dates()
            stock.get_data()
            img = stock.plot_ts(plot_ma=True, plot_intervals=True, window=30, figsize=(20,13))
            app.logger.info("Got data for "+symbol)
            
            if flask.request.method == 'POST':
                ### input dal client
                window = int(flask.request.form["window"])
                neurons = int(flask.request.form["neurons"])
                ahead = int(flask.request.form["ahead"])
                ### preprocessing
                model = lstm(stock.ts, size=window)
                model.ts_preprocessing(scaler=None)
                model.fit_lstm(units=neurons)
                img = model.predict_lstm(ts=stock.ts, ahead=ahead)
                dtf = model.dtf[ pd.notnull(model.dtf["pred"]) ][["pred"]].reset_index(drop=True)
                return flask.render_template("model.html", img=img, dtf=dtf)
            
            else:
                return flask.render_template("model.html", img=img, dtf=None)
        except Exception as e:
            app.logger.error(e)
            flask.abort(500)
    
    
    ## errors
    @app.errorhandler(404)
    def page_not_found(e):
        return flask.render_template("errors.html", msg="Page doesn't exist"), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return flask.render_template('errors.html', msg="Something went terribly wrong"), 500
    
    
    return app