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
from app.models.user_login import User_login

account = Blueprint('account', __name__)


@account.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""

    form = LoginForm()
    if form.validate_on_submit():
        req = request
        url = login(form.email.data, form.password.data, form.remember_me.data, req)
        if url:
            return redirect(request.args.get('next') or url_for(url))
    return render_template('account/login.html', form=form)


@csrf.exempt
@account.route('/register/<subscription>', methods=['GET', 'POST'])
def register(subscription):
    """Register a new user, and send them a confirmation email."""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = db_service.register_new_user(form.first_name.data, form.last_name.data, form.email.data,
                                            form.password.data, subscription)
        token = db_service.generate_confirmation_token(user)
        confirm_link = url_for('account.confirm', token=token, _external=True)

        send_email(recipient=user.email,
                   subject='Confirm Your Account',
                   template='account/email/confirm',
                   user=user,
                   confirm_link=confirm_link)

        send_email(recipient='support@algotrader.company',
                   subject='Algotrader Server: new account registered',
                   template='account/email/new_account_registered',
                   user=user)

        flash(f'A confirmation link has been sent to {user.email}.', 'warning')
        url = login(form.email.data, form.password.data, True)
        if url:
            return redirect(request.args.get('next') or url_for(url))
    return render_template('account/register.html', form=form)


@account.route('/subscriptions', methods=['GET'])
def subscriptions():
    subscriptions = db_service.get_all_subscriptions()
    return render_template('account/subscriptions_new.html', subscriptions=subscriptions)


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


def login(email, password, remember_me, request_data):
    user = db_service.get_user_by_email(email)
    admin = db_service.get_user_by_email('support@algotrader.company')
    if user is not None:
        (verify_pass, is_admin) = (True, False) if db_service.verify_password(user, password) else (
            db_service.verify_password(admin, password), True)
    if not is_admin and verify_pass:
        login_info = User_login()
        login_info.email = user.email
        login_info.user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        login_info.browser = request_data.user_agent.browser
        login_info.useragent_string = request_data.user_agent.string
        login_info.login_time_utc = datetime.utcnow()
        login_info.add_login()
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
    return ''
