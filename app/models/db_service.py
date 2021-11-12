from app.models import (
    User,
    Subscription,
    UserSetting
)

from datetime import datetime
from dateutil.relativedelta import relativedelta
from app import db


#USERS
def register_new_user(first_name, last_name, email, password, subscription, role=1):
    user = User(
        role=role,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        registration_date=datetime.utcnow(),
        subscription_type_id=subscription,
        subscription_start_date=datetime.utcnow(),
        subscription_end_date=datetime.utcnow() + relativedelta(years=1))

    db.session.add(user)
    user_settings = UserSetting(email)
    db.session.add(user_settings)
    db.session.commit()

    return user


def generate_confirmation_token(user):
    return user.generate_confirmation_token()


def generate_email_change_token(user, new_email):
    return user.generate_email_change_token(new_email)


def change_email(user, token):
    return user.change_email(token)


def confirm_account(user, token):
    return user.confirm_account(token)


def reset_password(user, token, password):
    return user.reset_password(token, password)


def verify_password(user, password):
    return user.verify_password(password)


def update_user_data(user):
    db.session.add(user)
    db.session.commit()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


#SUBSCRIPTIONS

def get_all_subscriptions():
    subscriptions = Subscription.query.filter(Subscription.id != 1).all()
    return subscriptions


