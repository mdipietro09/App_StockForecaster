###############################################################################
#                                MAIN                                         #
###############################################################################

import flask
import pickle
from tensorflow.keras import models
import pandas as pd

from model.data import data
from model.lstm import lstm
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
    #app.config.from_pyfile("config/app_settings.py", silent=True)
    
    
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
                ## save data
                pickle_out = open(dirpath+'instance/ts.pickle', mode="wb")
                pickle.dump(stock.ts, pickle_out)
                pickle_out.close()
                #return flask.send_file(img, attachment_filename='plot.png', mimetype='image/png')
                return flask.render_template("data.html", img=img)
            else:
                return flask.render_template("data.html")
        except Exception as e:
            app.logger.error(e)
            flask.abort(500)
    
    @app.route("/model", methods=['GET', 'POST'])
    def train_model():
        try:
            if flask.request.method == 'POST':
                ### load data
                ts = pickle.load( open(dirpath+'instance/ts.pickle', mode="rb") )
                ### input dal client
                window = int(flask.request.form["window"])
                batch_size = int(flask.request.form["batch_size"])
                epochs = int(flask.request.form["epochs"])
                neurons = int(flask.request.form["neurons"])
                ahead = int(flask.request.form["ahead"])
                ### preprocessing
                model = lstm(ts, size=window)
                model.ts_preprocessing(scaler=None)
                model.fit_lstm(batch_size=batch_size, epochs=epochs, units=neurons)
                img = model.predict_lstm(ts=ts, ahead=ahead)
                dtf = model.dtf[ pd.notnull(model.dtf["pred"]) ][["pred"]].reset_index(drop=True)
                return flask.render_template("model.html", img=img, dtf=dtf.to_html())
            else:
                return flask.render_template("model.html")
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