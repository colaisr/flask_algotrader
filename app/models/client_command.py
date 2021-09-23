from .. import db


class ClientCommand(db.Model):
    __tablename__ = 'ClientCommands'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String)
    command = db.Column('command', db.String)

    def __init__(self, email):
        self.email = email
        self.command = 'run_worker'

    def add_commannd(self):
        db.session.add(self)
        db.session.commit()

    def set_command(self, command):
        self.command = command
        db.session.commit()

    def set_restart(self):
        self.command = "restart_worker"
        db.session.commit()

    def set_run_worker(self):
        self.command = "run_worker"
        db.session.commit()

    def set_close_all_positions(self):
        self.command = "close_all_positions"
        db.session.commit()
