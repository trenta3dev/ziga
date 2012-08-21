import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask.ext.script import Manager, Server

from ziga import app

manager = Manager(app)


manager.add_command('runserver',  Server(port=4242))


if __name__ == "__main__":
    manager.run()
