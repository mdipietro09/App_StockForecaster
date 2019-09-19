
import pandas as pd
import numpy as np
from sklearn import preprocessing
from tensorflow.keras import models, layers
import matplotlib.pyplot as plt
import io
import base64



class lstm():
    
    def __init__(self, ts, size):
        self.ts = ts
        self.size = size
        
        
    def ts_preprocessing(self, scaler=None):
        self.ts = self.ts.sort_index(ascending=True).values
        self.scaler = preprocessing.MinMaxScaler(feature_range=(0,1))          
        ts_preprocessed = self.scaler.fit_transform(self.ts.reshape(-1,1))          
        
        ## create X y for train
        lst_X, lst_y = [], []
        for i in range(len(ts_preprocessed)):
            end_ix = i + self.size
            if end_ix > len(ts_preprocessed)-1:
                break
            Xi, yi = ts_preprocessed[i:end_ix], ts_preprocessed[end_ix]
            lst_X.append(Xi)
            lst_y.append(yi)
        X = np.array(lst_X)
        self.y = np.array(lst_y)
        self.X = np.reshape(X, (X.shape[0], 1, X.shape[1]))
        
    
    def fit_lstm(self, batch_size=32, epochs=100, units=50, figsize=(20,13)):
        ## lstm
        model = models.Sequential()
        model.add( layers.LSTM(input_shape=self.X.shape[1:], units=units, activation='tanh', return_sequences=False) )
        model.add( layers.Dense(1) )
        model.compile(optimizer='rmsprop', loss='mean_squared_error')
        
        ## fit
        training = model.fit(x=self.X, y=self.y, batch_size=batch_size, epochs=epochs, shuffle=True, verbose=0)
        self.model = training.model
        
        ## plot
        #fig, ax = plt.subplots(figsize=figsize)
        #ax.plot(training.history['loss'], label='loss')
        #plt.xlabel('epoch')
        #plt.legend()
        #bytes_image = io.BytesIO()
        #plt.savefig(bytes_image, format='png')
        #bytes_image.seek(0)
        #bytes_image_url = base64.b64encode(bytes_image.getvalue()).decode()
        #return 'data:image/png;base64,{}'.format(bytes_image_url)
    
    
    def predict_lstm(self, ts, ahead=5, figsize=(20,13)):
        ## preprocess
        ts = ts.sort_index(ascending=True).values
        ts_preprocessed = list(self.scaler.fit_transform(ts.reshape(-1,1)))
        
        ## validation
        lst_fitted = [np.nan]*self.size
        for i in range(len(ts_preprocessed)):
            end_ix = i + self.size
            if end_ix > len(ts_preprocessed)-1:
                break
            X = ts_preprocessed[i:end_ix]
            X = np.array(X)
            X = np.reshape(X, (1, 1, X.shape[0]))
            fit = self.model.predict(X)
            fit = self.scaler.inverse_transform(fit)[0][0]
            lst_fitted.append(fit)
             
        ## predict
        lst_preds = []
        for i in range(ahead):
            i += 1
            lst_X = ts_preprocessed[len(ts_preprocessed)-(self.size+1) : -1]
            X = np.array(lst_X)
            X = np.reshape(X, (1, 1, X.shape[0]))
            pred = self.model.predict(X)
            ts_preprocessed.append(pred)
            pred = self.scaler.inverse_transform(pred)[0][0]
            lst_preds.append({"actual":np.nan, "pred":pred})
            
        ## plot
        dtf = pd.DataFrame({'actual':ts, 'fitted':lst_fitted, 'pred':np.nan})
        dtf = pd.concat( [dtf, pd.DataFrame([dic for dic in lst_preds])] )
        self.dtf = dtf.reset_index(drop=True)
        ax = self.dtf.plot(title="pred "+str(ahead)+" ahead", figsize=figsize, linewidth=3)
        ax.grid(True)
        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        bytes_image_url = base64.b64encode(bytes_image.getvalue()).decode()
        return 'data:image/png;base64,{}'.format(bytes_image_url)
        
        