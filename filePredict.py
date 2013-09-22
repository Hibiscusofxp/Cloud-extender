import httplib2
import time


from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import client

class Ohnoauth():
    
    def __init__(self):
        
        #Class Vars
        self.CLIENT_ID = '189438750868.apps.googleusercontent.com'
        self.CLIENT_SECRET = 'iNuKAa92i1NOgBIusK2rW5FL'
        self.OAUTH_SCOPE = 'https://www.googleapis.com/auth/prediction https://www.googleapis.com/auth/devstorage.full_control'
        self.REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
        self.PROJECT = 189438750868
        self.ID = 13
        self.STORAGEDATALOCATION = 'cloudextender/m2.csv'
        self.SLEEP_TIME = 10

        flow = OAuth2WebServerFlow(self.CLIENT_ID, self.CLIENT_SECRET, self.OAUTH_SCOPE, self.REDIRECT_URI)
        authorize_url = flow.step1_get_authorize_url()
        print 'Go to the following link in your browser: ' + authorize_url
        code = raw_input('Enter verification code: ').strip()
        credentials = flow.step2_exchange(code)

        # Create an httplib2.Http object and authorize it with our credentials
        http = httplib2.Http()
        http = credentials.authorize(http)
        self.predict_service = build('prediction', 'v1.6', http=http)

    def getPrediction(self, strg):
        #gets query from prediction API
        try:
            papi = self.predict_service.trainedmodels()
            body = {'input': {'csvInstance': [strg]}}
            result = papi.predict(body=body, id=self.ID, project=self.PROJECT).execute()

            return result

        except client.AccessTokenRefreshError:
            print ("The credentials have been revoked or expired, please re-run"
                   "the application to re-authorize")
            return
        
    def train(self):
        #trains Prediction API based on file at self.STORAGEDATALOCATION
        body = {'id': self.ID, 'storageDataLocation': self.STORAGEDATALOCATION}
        papi = self.predict_service.trainedmodels()
        papi.insert(body=body, project=self.PROJECT).execute()
        
        while True:
            status = papi.get(id=self.ID, project=self.PROJECT).execute()
            state = status['trainingStatus']
            if state == 'DONE':
                break
            elif state == 'RUNNING':
                time.sleep(self.SLEEP_TIME)
                continue
            else:
                raise Exception('Training Error: ' + state)
                break
            return
        
        