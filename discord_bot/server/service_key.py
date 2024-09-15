import os

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
project_dir = os.path.dirname(parent_dir)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(project_dir, 'creds', 'ServiceKey_GoogleCloud.json')