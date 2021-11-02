import requests
from requests.models import ReadTimeoutError

class PyspectiveAPI():
    def __init__(self, APIkey):
        self.key = APIkey
    def score(self,comment,test:str=None):
        allowedTest = ["TOXICITY",
            'SEVERE_TOXICITY',
            'IDENTITY_ATTACK',
            'INSULT',
            'PROFANITY',
            'THREAT',
            'SEXUALLY_EXPLICIT',
            'FLIRTATION']
        url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={self.key}'
        if test is None:
            postMe =   {
                "comment": {
                    "text": comment
                    },
                "languages": ["en"],
                "requestedAttributes": {
                    "TOXICITY": {},
                    'SEVERE_TOXICITY':{},
                    'IDENTITY_ATTACK':{},
                    'INSULT':{},
                    'PROFANITY':{},
                    'THREAT':{},
                    'SEXUALLY_EXPLICIT':{},
                    'FLIRTATION':{}
                    }
                }
        else:
            if test.upper() not in allowedTest:
                return 
            postMe =   {
                "comment": {
                    "text": comment
                    },
                "languages": ["en"],
                "requestedAttributes": {
                    test.upper(): {},
                    }
                }
        r = requests.post(url=url,json=postMe)
        scoreOverview = r.json()["attributeScores"]
        score = {}
        for x in scoreOverview:
            score[x] = scoreOverview[x]["summaryScore"]["value"]
        return score
    def suggest(self,text:str,score:float):
            url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:suggestscore?key={self.key}'
            postMe = {
                "comment": {
                    "text": text
                    },
                "attributeScores": {
                    "TOXICITY": {
                    "summaryScore": {
                        "value": score
                        }
                    },
                },
                }
            r = requests.post(url=url,json=postMe,timeout=2.0)
            if r.status_code == 200:
                return 'Successed'
