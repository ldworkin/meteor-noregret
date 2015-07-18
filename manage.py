import yaml
import mturk
import os
from pymongo import MongoClient

sandbox = False

params = yaml.load(open('params.txt'))

key = params['my_key']
secret = params['my_secret']

config = {'use_sandbox': sandbox,
          'stdout_log': False,
          'verify_mturk_ssl': True,
          'aws_key': key,
          'aws_secret_key': secret}

m = mturk.MechanicalTurk(config)

client = MongoClient('mongodb://127.0.0.1:3001')
db = client.meteor
                
question = """
<ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
<ExternalURL>https://test.lilianne.me</ExternalURL>
<FrameHeight>600</FrameHeight>
</ExternalQuestion>
"""

qualifications = [
    {'QualificationTypeId': mturk.LOCALE,
     'Comparator': 'In',
     'LocaleValue': [{'Country': 'US'}, {'Country':'CA'}, {'Country':'IN'}]},
     {'QualificationTypeId': mturk.P_APPROVED,
      'Comparator': 'GreaterThanOrEqualTo',
      'IntegerValue': 95},
     {'QualificationTypeId': mturk.N_APPROVED,
      'Comparator': 'GreaterThanOrEqualTo',
      'IntegerValue': 100}
      ]
                            
def create_hit():
    hit = {'Title': 'Prediction Experiment',
           'Description': 'In this HIT you will play a sequence of games and earn a bonus based on the decisions you make.',
           'Keywords': 'experiment,decision-making',
           'Question': question,
           'Reward': {'Amount': 0.25, 'CurrencyCode': 'USD'},
           'LifetimeInSeconds': 60*60*24,
           'AssignmentDurationInSeconds': 4*60*60,
           'MaxAssignments': 2,
           'AutoApprovalDelayInSeconds': 60,
           'QualificationRequirement': qualifications}
    r = m.request('CreateHIT', hit)
    print r


def print_users():
    users = db.users.find()
    for user in users:
        if user['state'] == 'game':
            print 'Username: %s' % user['username']
            print 'State: %s' % user['state']        
            print 'Score: %d' % user['score']
            print 'Online: %s' % user['status']['online']
            print 'Paid: %s' % user.get('paid')
            print

def grant_bonus():
    users = db.users.find()
    for user in users:
        if user['assignmentId'] and 'paid' not in user and user['score']:
            amt = '%.2f' % (user['score']*0.005)
            bonus = {'Operation': 'GrantBonus',
                     'WorkerId': user['username'],
                     'AssignmentId': user['assignmentId'],
                     'BonusAmount': {'Amount': amt, 'CurrencyCode': 'USD'},
                     'Reason': 'Bonus for prediction HIT. Thanks for participating!'}
            db.users.update_one({'username': user['username']}, {'$set': {'paid': True}})
            r = m.request('GrantBonus', bonus)
            print r

def create_qual(name, desc):
    qual = {'Operation': 'CreateQualificationType',
            'Name': name,
            'Description': desc,
            'QualificationTypeStatus': 'Active'}
    r = m.request('CreateQualificationType', qual)
    print r

def assign_qual(qualId, workerId):
    qual = {'Operation': 'AssignQualification',
            'QualificationTypeId': qualId,
            'WorkerId': workerId}
    r = m.request('AssignQualification', qual)
    print r

def notify(subject, text, workerId):
    notify = {'Operation': 'NotifyWorkers',
              'Subject': subject,
              'MessageText': text,
              'WorkerId': workerId}
    r = m.request('NotifyWorkers', notify)
    print r
