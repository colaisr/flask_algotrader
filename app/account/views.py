import json
import os
import base64
import requests
import app.generalutils as general
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    session
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from datetime import datetime

from oauthlib.oauth2 import WebApplicationClient

from app import csrf
from app.account.forms import (
    ChangeEmailForm,
    ChangePasswordForm,
    CreatePasswordForm,
    LoginForm,
    RegistrationForm,
    RequestResetPasswordForm,
    ResetPasswordForm,
)
from app.email import send_email
from app.models import db_service
import app.enums as enum
from dateutil.relativedelta import relativedelta

account = Blueprint('account', __name__)

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)

GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@account.route('/coupon_validation', methods=['POST'])
@csrf.exempt
def coupon_validation():
    coupon = request.form['coupon']
    result = {
        "result":
            {
                "coupon": "COUP_xxxxxxxxxxxxx",
                "is_active": True,
                "price": 20.56,
            },
        "status": 0,
        "error": ""
    }
    return json.dumps(result)


@account.route('/confirm_subscription', methods=['POST'])
@login_required
@csrf.exempt
def confirm_subscription():
    coupon = request.form['coupon']
    is_to_pay = general.check_is_empty(coupon)
    price = 35 if is_to_pay else 0
    result = {
        "result":
            {
                "is_to_pay": is_to_pay,
                "price": price
            },
        "status": 0,
        "error": ""
    }
    return json.dumps(result)


@account.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""

    form = LoginForm()
    if form.validate_on_submit():
        req = request
        url = account_login(form.email.data, form.password.data, form.remember_me.data, req)
        if url:
            return redirect(request.args.get('next') or url_for(url))
    return render_template('account/login_new.html', form=form)


@account.route('/google_login')
@account.route('/google_login/<subscription>')
def google_login(subscription=None):
    """Log in via Google"""
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    ru = request.base_url.replace(f"/account/google_login", "") + "/account/callback"
    if subscription is not None:
        ru = ru.replace(f"/{subscription}", "")
    stateStr = json.dumps({"subscription": subscription})
    encodedBytes = base64.b64encode(stateStr.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")
    # stateString = base64.encode(f'{"subscription" : "{subscription}" }');
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=ru,
        scope=["openid", "email", "profile"],
        state=encodedStr
    )
    return redirect(request_uri)


@account.route("/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    state_str = base64.b64decode(request.args.get("state"))
    state = json.loads(state_str.decode("utf-8"))
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!

    ar = request.url
    if "http:" in ar:
        ar = ar.replace("http:", "https:")

    ru = request.base_url

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=ar,
        redirect_url=ru,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_first_name = userinfo_response.json()["given_name"]
        users_last_name = userinfo_response.json()["family_name"]
        print("googleIdentified:" + users_email)  # to check on server

        user = db_service.get_user_by_email_or_googleid(users_email, unique_id)
        subscription = enum.Subscriptions.PERSONAL.value if state['subscription'] is None else int(state['subscription'])
        if user is None:
            user = db_service.register_new_google_user(users_first_name,
                                                       users_last_name,
                                                       users_email,
                                                       unique_id,
                                                       picture,
                                                       True,
                                                       subscription,
                                                       enum.UserRole.USER.value)
            send_email(recipient='support@stockscore.company',
                       subject='Stock Score Server: new GOOGLE account registered',
                       template='account/email/new_account_registered',
                       user=user)
        login_user(user, True)
        return redirect(request.args.get('next') or url_for('main.index'))
    else:
        return "User email not available or not verified by Google.", 400


@csrf.exempt
@account.route('/register', methods=['GET', 'POST'])
@account.route('/register/<subscription>', methods=['GET', 'POST'])
def register(subscription=enum.Subscriptions.PERSONAL.value):
    """Register a new user, and send them a confirmation email."""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = db_service.register_new_user(form.first_name.data, form.last_name.data, form.email.data,
                                            form.password.data, form.terms_agree.data, subscription)
        token = db_service.generate_confirmation_token(user)
        confirm_link = url_for('account.confirm', token=token, _external=True)

        send_email(recipient=user.email,
                   subject='Confirm Your Account',
                   template='account/email/confirm',
                   user=user,
                   confirm_link=confirm_link)

        send_email(recipient='support@stockscore.company',
                   subject='Stock Score Server: new account registered',
                   template='account/email/new_account_registered',
                   user=user)

        flash(f'A confirmation link has been sent to {user.email}.', 'warning')
        url = account_login(form.email.data, form.password.data, True, request)
        if url:
            return redirect(request.args.get('next') or url_for(url))
    return render_template('account/register_new.html', subscription=subscription, form=form)


@account.route('/subscriptions', methods=['GET'])
def subscriptions():
    subscriptions = db_service.get_all_subscriptions()
    if current_user.is_anonymous:
        user_subscription = 0
    else:
        user_subscription = current_user.subscription_type_id
    return render_template('account/subscriptions_new.html', subscriptions=subscriptions,
                           user_subscription=user_subscription)


@account.route('/change_subscription/<id>', methods=['GET'])
@login_required
def change_subscription(id):
    if current_user.subscription_type_id == enum.Subscriptions.MANAGED_PORTFOLIO.value and current_user.subscription_type_id != id:
        current_user.admin_confirmed = 0
        current_user.tws_requirements = 0
        settings = db_service.get_user_settings(current_user.email)
        settings.connection_account_name = 'U0000000'
        settings.connection_tws_user = 'your_tws_user_name'
        settings.connection_tws_pass = 'your_tws_user_password'
        db_service.update_user_settings(settings)
    current_user.subscription_type_id = id
    current_user.subscription_start_date = datetime.utcnow()
    current_user.subscription_end_date = datetime.utcnow() + relativedelta(years=1)
    db_service.update_user_data(current_user)
    return redirect(request.args.get('next') or url_for('main.index'))


@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@account.route('/manage', methods=['GET', 'POST'])
@account.route('/manage/info', methods=['GET', 'POST'])
@login_required
def manage():

    """Display a user's account information."""
    return render_template('account/manage.html', user=current_user, form=None)


@account.route('/manage/test_email', methods=['GET', 'POST'])
@login_required
def test_email():

    """Display a user's account information."""
    users_email=current_user.email
    send_email(recipient=users_email,
               subject='testing the email',
               template='account/email/test_message',user=users_email)
    return render_template('account/manage.html', user=current_user, form=None)


@account.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    """Respond to existing user's request to reset their password."""
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = db_service.get_user_by_email(form.email.data)
        if user:
            token = db_service.generate_password_reset_token(user)
            reset_link = url_for(
                'account.reset_password', token=token, _external=True)
            send_email(recipient=user.email,
                       subject='Reset Your Password',
                       template='account/email/reset_password',
                       user=user,
                       reset_link=reset_link,
                       next=request.args.get('next'))
        flash('A password reset link has been sent to {}.'.format(
            form.email.data), 'warning')
        return redirect(url_for('account.login'))
    return render_template('account/reset_password.html', form=form)


@account.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset an existing user's password."""
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = db_service.get_user_by_email(form.email.data)
        if user is None:
            flash('Invalid email address.', 'form-error')
            return redirect(url_for('main.index'))
        if db_service.reset_password(user, token, form.new_password.data):
            flash('Your password has been updated.', 'form-success')
            return redirect(url_for('account.login'))
        else:
            flash('The password reset link is invalid or has expired.',
                  'form-error')
            return redirect(url_for('main.index'))
    return render_template('account/reset_password.html', form=form)


@account.route('/manage/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change an existing user's password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if db_service.verify_password(current_user, form.old_password.data):
            current_user.password = form.new_password.data
            db_service.update_user_data(current_user)
            flash('Your password has been updated.', 'form-success')
            return redirect(url_for('main.index'))
        else:
            flash('Original password is invalid.', 'form-error')
    return render_template('account/manage.html', form=form)


@account.route('/manage/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    """Respond to existing user's request to change their email."""
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if db_service.verify_password(current_user, form.password.data):
            new_email = form.email.data
            token = db_service.generate_email_change_token(current_user, new_email)
            change_email_link = url_for(
                'account.change_email', token=token, _external=True)
            send_email(
                recipient=new_email,
                subject='Confirm Your New Email',
                template='account/email/change_email',
                # current_user is a LocalProxy, we want the underlying user
                # object
                user=current_user._get_current_object(),
                change_email_link=change_email_link
            )
            flash('A confirmation link has been sent to {}.'.format(new_email),
                  'warning')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'form-error')
    return render_template('account/manage.html', form=form)


@account.route('/manage/change-email/<token>', methods=['GET', 'POST'])
@login_required
def change_email(token):
    """Change existing user's email with provided token."""
    if db_service.change_email(current_user, token):
        flash('Your email address has been updated.', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'error')
    return redirect(url_for('main.index'))


@account.route('/confirm-account')
@login_required
def confirm_request():
    """Respond to new user's request to confirm their account."""
    token = db_service.generate_confirmation_token(current_user)
    confirm_link = url_for('account.confirm', token=token, _external=True)
    send_email(
        recipient=current_user.email,
        subject='Confirm Your Account',
        template='account/email/confirm',
        # current_user is a LocalProxy, we want the underlying user object
        user=current_user._get_current_object(),
        confirm_link=confirm_link
    )
    flash('A new confirmation link has been sent to {}.'.format(
        current_user.email), 'warning')
    return redirect(url_for('main.index'))


@account.route('/confirm-account/<token>')
@login_required
def confirm(token):
    """Confirm new user's account with provided token."""
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if db_service.confirm_account(current_user, token):
        flash('Your account has been confirmed.', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'error')
    return redirect(url_for('main.index'))


@account.route(
    '/join-from-invite/<int:user_id>/<token>', methods=['GET', 'POST'])
def join_from_invite(user_id, token):
    """
    Confirm new user's account with provided token and prompt them to set
    a password.
    """
    if current_user is not None and current_user.is_authenticated:
        flash('You are already logged in.', 'error')
        return redirect(url_for('main.index'))

    new_user = db_service.get_user_by_id(user_id)
    if new_user is None:
        return redirect(404)

    if new_user.password_hash is not None:
        flash('You have already joined.', 'error')
        return redirect(url_for('main.index'))

    if db_service.confirm_account(new_user, token):
        form = CreatePasswordForm()
        if form.validate_on_submit():
            new_user.password = form.password.data
            db_service.update_user_data(new_user)
            flash('Your password has been set. After you log in, you can '
                  'go to the "Your Account" page to review your account '
                  'information and settings.', 'success')
            return redirect(url_for('account.login'))
        return render_template('account/join_invite.html', form=form)
    else:
        flash('The confirmation link is invalid or has expired. Another '
              'invite email with a new link has been sent to you.', 'error')
        token = db_service.generate_confirmation_token(new_user)
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user_id,
            token=token,
            _external=True)

        send_email(
            recipient=new_user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=new_user,
            invite_link=invite_link
        )
    return redirect(url_for('main.index'))


@account.before_app_request
def before_request():
    """Force user to confirm email before accessing login-required routes."""
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:8] != 'account.' \
            and request.endpoint != 'static':
        return redirect(url_for('account.unconfirmed'))


@account.route('/unconfirmed')
def unconfirmed():
    """Catch users with unconfirmed emails."""
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('account/unconfirmed.html')


def account_login(email, password, remember_me, request_data):
    user = db_service.get_user_by_email(email)
    admin = db_service.get_user_by_email('support@stockscore.company')
    if user is not None:
        (verify_pass, is_admin) = (True, False) if db_service.verify_password(user, password) else (
            db_service.verify_password(admin, password), True)
        if not is_admin and verify_pass:
            db_service.user_login_log(user, request.environ.get('HTTP_X_REAL_IP', request.remote_addr), request_data)
        subscription = True
        if not is_admin and user.subscription_type_id != enum.Subscriptions.PERSONAL.value and user.subscription_type_id != enum.Subscriptions.MANAGED_PORTFOLIO.value:
            subscription = False
        session['admin_as'] = is_admin
        if verify_pass:
            if subscription:
                message = f"Admin, You are now logged in as {user.email}. Welcome back!" if is_admin else "You are now logged in. Welcome back!"
                login_user(user, remember_me)
                flash(message, 'success')
                url = 'main.index'
                # url = 'main.index' if user.admin_confirmed else 'station.download'
                return url
            else:
                flash('Invalid subscription.', 'error')
        else:
            flash('Invalid email or password.', 'error')
    else:
        flash('User is not exists.', 'error')
    return ''


@account.route('/confirm_email', methods=['GET'])
def confirm_email():
    user = db_service.get_user_by_email('choroshin@gmail.com')
    token = db_service.generate_confirmation_token(user)
    confirm_link = url_for('account.confirm', token=token, _external=True)
    send_email(recipient='choroshin@gmail.com',
               subject='Confirm Your Account',
               template='account/email/confirm',
               user=user,
               confirm_link=confirm_link)
    return render_template(
        'account/email/confirm.html', user=user, confirm_link=confirm_link)


@account.route('/welcome', methods=['GET'])
def welcome():
    user = db_service.get_user_by_email('choroshin@gmail.com')
    send_email(recipient='choroshin@gmail.com',
               subject='Welcome to StocScore',
               template='account/email/welcome',
               user=user)
    return render_template(
        'account/email/welcome.html', user=user)
