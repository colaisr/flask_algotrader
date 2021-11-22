import app.enums as enum
from app.models import (
    User,
    Subscription,
    UserSetting,
    Tooltip
)
from app.models.user_login import User_login
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app import db
from sqlalchemy import text, or_, and_


#USERS
def register_new_user(first_name, last_name, email, password, terms_agree, subscription, role=1):
    user = User(
        role_id=role,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        signature=terms_agree,
        signature_full_name=f"{first_name} {last_name}",
        registration_date=datetime.utcnow(),
        subscription_type_id=subscription,
        subscription_start_date=datetime.utcnow(),
        subscription_end_date=datetime.utcnow() + relativedelta(years=1))

    db.session.add(user)
    user_settings = UserSetting(email)
    db.session.add(user_settings)
    db.session.commit()

    return user


def register_new_google_user(first_name, last_name, email, google_id, google_img, terms_agree, subscription, role=1):
    user = User(
        role_id=role,
        first_name=first_name,
        last_name=last_name,
        email=email,
        google_id=google_id,
        google_account_img=google_img,
        signature=terms_agree,
        signature_full_name=f"{first_name} {last_name}",
        registration_date=datetime.utcnow(),
        subscription_type_id=subscription,
        subscription_start_date=datetime.utcnow(),
        subscription_end_date=datetime.utcnow() + relativedelta(years=1),
        confirmed=True)

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


def generate_password_reset_token(user):
    return user.generate_password_reset_token()


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


def get_user_by_email_or_googleid(email, googleid):
    return User.query.filter(or_(User.email == email, User.google_id == googleid)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


#LOGIN LOG
def user_login_log(user, user_ip, request_data):
    login_info = User_login()
    login_info.email = user.email
    login_info.user_ip = user_ip
    login_info.browser = request_data.user_agent.browser
    login_info.useragent_string = request_data.user_agent.string
    login_info.login_time_utc = datetime.utcnow()
    login_info.add_login()


#SUBSCRIPTIONS
def get_all_subscriptions():
    subscriptions = Subscription.query.filter(Subscription.id != 1).all()
    return subscriptions


#SETTINGS
def get_user_settings(email):
    return UserSetting.query.filter_by(email=email).first()


def update_user_settings(settings):
    settings.update_user_settings()


#TOOLTIPS
def get_tooltips():
    return Tooltip.query.all()



