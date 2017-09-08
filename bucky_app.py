import os
from bucky import create_app
import click

from bucky.models import Task, BucketList, User, AppManager

am = AppManager()
app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, AppManager=AppManager, User=User, BucketList=BucketList, Task=Task)
