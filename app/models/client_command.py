from .. import db

class ClientCommand(db.Model):
    __tablename__ = 'ClientCommands'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String)
    command = db.Column('command', db.String)


    def add_commannd(self):
        db.session.add(self)
        db.session.commit()

    def set_command(self,command):
        c = ClientCommand.query.filter_by(email=self.email).first()
        c.command=command
        db.session.commit()

    def set_restart(self):
        c = ClientCommand.query.filter_by(email=self.email).first()
        c.command="restart_worker"
        db.session.commit()

    def set_run_worker(self):
        c = ClientCommand.query.filter_by(email=self.email).first()
        c.command="run_worker"
        db.session.commit()

    def set_close_all_positions(self):
        c = ClientCommand.query.filter_by(email=self.email).first()
        c.command="close_all_positions"
        db.session.commit()