import yaml
import mturk
import os
from pymongo import MongoClient

sandbox = True

params = yaml.load(open('params.txt'))

key = params['my_key']
secret = params['my_secret']

config = {'use_sandbox': sandbox,
          'stdout_log': False,
          'verify_mturk_ssl': True,
          'aws_key': key,
          'aws_secret_key': secret}

m = mturk.MechanicalTurk(config)

client = MongoClient(params['mongoURI'])
db = client.tiZud2yh

def dump_db():
    # make sure to run mongod in another tab first
    os.system('./dump.sh lilidworkin.meteor.com')

def print_users():
    users = db.users.find()
    for user in users:
        print user['username']
        print 'assignmentId: ' + str(user['assignmentId'])
        print 'score: ' + str(user['score'])
        print

    
question = """
<ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
<ExternalURL>https://lilidworkin.meteor.com</ExternalURL>
<FrameHeight>600</FrameHeight>
</ExternalQuestion>
"""

qualifications = [
    {'QualificationTypeId': mturk.LOCALE,
     'Comparator': 'In',
     'LocaleValue': [{'Country': 'US'}, {'Country':'CA'}]},
     {'QualificationTypeId': mturk.P_APPROVED,
      'Comparator': 'GreaterThanOrEqualTo',
      'IntegerValue': 95}
      ]
                            
def create_hit():
    hit = {'Title': 'Prediction Experiment',
           'Description': 'In this HIT you will play a sequence of games and earn a bonus based on the decisions you make.',
           'Keywords': 'experiment,decision-making',
           'Question': question,
           'Reward': {'Amount': 0.25, 'CurrencyCode': 'USD'},
           'LifetimeInSeconds': 60*60*24,
           'AssignmentDurationInSeconds': 60*60,
           'MaxAssignments': 1,
           'AutoApprovalDelayInSeconds': 60,
           'QualificationRequirement': []}
    r = m.request('CreateHIT', hit)
    print r
                                        
                                        
def get_hits():
    get = {'Operation': 'SearchHITs'}
    r = m.request('SearchHITs', get)
    return r['SearchHITsResponse']['SearchHITsResult']['HIT']
        
        
def delete_hits():
    get = {'Operation': 'SearchHITs'}
    r = m.request('SearchHITs', get)
    hitobjs = r['SearchHITsResponse']['SearchHITsResult']['HIT']
    if isinstance(hitobjs, dict):
        hitobjs = [hitobjs]
        hits = [x['HITId'] for x in hitobjs]
        for hit in hits:
            expire = {'Operation': 'ForceExpireHIT',
                      'HITId': hit}
            r = m.request('ForceExpireHIT', expire)
            delete = {'Operation': 'DisposeHIT',
                      'HITId': hit}
            r = m.request('DisposeHIT', delete)
                    
def grant_bonus():
    users = db.users.find()
    for user in users:
        if user['assignmentId']:
            amt = '%.2f' % (user['score']*0.005)
            bonus = {'Operation': 'GrantBonus',
                     'WorkerId': user['username'],
                     'AssignmentId': user['assignmentId'],
                     'BonusAmount': {'Amount': amt, 'CurrencyCode': 'USD'},
                     'Reason': 'Bonus for prediction HIT'}
            r = m.request('GrantBonus', bonus)
            print r
