from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_rq import get_queue
from sqlalchemy import select, distinct, text, func

from app import db
from app import csrf
from app.admin.forms import (
    ChangeAccountTypeForm,
    ChangeUserEmailForm,
    InviteUserForm,
    NewUserForm,
)
from app.decorators import admin_required
from app.email import send_email
from app.models import EditableHTML, Role, User, TickerData, UserSetting, ClientCommand

admin = Blueprint('admin', __name__)


@admin.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard page."""
    return render_template('admin/index.html')


@admin.route('/new-user', methods=['GET', 'POST'])
@login_required
@admin_required
def new_user():
    """Create a new user."""
    form = NewUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User {} successfully created'.format(user.full_name()),
              'form-success')
    return render_template('admin/new_user.html', form=form)


@admin.route('/invite-user', methods=['GET', 'POST'])
@login_required
@admin_required
def invite_user():
    """Invites a new user to create an account and set their own password."""
    form = InviteUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user.id,
            token=token,
            _external=True)

        send_email(
            recipient=user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=user,
            invite_link=invite_link,
        )
        # get_queue().enqueue(
        #     send_email,
        #     recipient=user.email,
        #     subject='You Are Invited To Join',
        #     template='account/email/invite',
        #     user=user,
        #     invite_link=invite_link,
        # )
        flash('User {} successfully invited'.format(user.full_name()),
              'form-success')
    return render_template('admin/new_user.html', form=form)


@admin.route('/users')
@login_required
@admin_required
def registered_users():
    """View all registered users."""
    users = User.query.all()
    roles = Role.query.all()
    return render_template(
        'admin/registered_users.html', users=users, roles=roles)

@admin.route('/pendingapproval')
@login_required
@admin_required
def pending_approval():
    """View all registered users."""
    users = User.query.filter_by(admin_confirmed=0).all()
    #roles = Role.query.all()
    return render_template(
        'admin/pending_approval.html', users=users)

@admin.route('/marketdata')
@login_required
@admin_required
def market_data():
    # #cleaning db
    # all=db.session.query(TickerData).all()
    # for k in all:
    #     i=2
    #     my_data = db.session.query(TickerData).filter(func.date(TickerData.updated_server_time) == k.updated_server_time.date(),TickerData.ticker==k.ticker).all()
    #     # same_dates=TickerData.query.filter_by(func.date(updated_server_time)=k.updated_server_time.date()).all()
    #     if len(my_data)>1:
    #         r=3
    #

    query_text="select a.* from Tickersdata a join (  select Tickersdata.`ticker`, max(Tickersdata.`updated_server_time`) as updated_server_time  from Tickersdata group by Tickersdata.`ticker`) b on b.`ticker`=a.`ticker` and b.`updated_server_time`=a.`updated_server_time`"
    r=db.session.query(TickerData).from_statement(text(query_text)).all()
    marketdata=r
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()
    for m in marketdata:
        if m.tipranks is None:
            m.tipranks=0

    return render_template('admin/market_data.html', user_settings=user_settings, marketdata=marketdata)

@admin.route('/clientcommands')
@login_required
@admin_required
def clientcommands():
    client_commands = ClientCommand.query.all()
    return render_template('admin/client_commands.html',client_commands=client_commands)


@admin.route('/user/<int:user_id>')
@admin.route('/user/<int:user_id>/info')
@login_required
@admin_required
def user_info(user_id):
    """View a user's profile."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/user/<int:user_id>/change-email', methods=['GET', 'POST'])
@login_required
@admin_required
def change_user_email(user_id):
    """Change a user's email."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    form = ChangeUserEmailForm()
    if form.validate_on_submit():
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Email for user {} successfully changed to {}.'.format(
            user.full_name(), user.email), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route(
    '/user/<int:user_id>/change-account-type', methods=['GET', 'POST'])
@login_required
@admin_required
def change_account_type(user_id):
    """Change a user's account type."""
    if current_user.id == user_id:
        flash('You cannot change the type of your own account. Please ask '
              'another administrator to do this.', 'error')
        return redirect(url_for('admin.user_info', user_id=user_id))

    user = User.query.get(user_id)
    if user is None:
        abort(404)
    form = ChangeAccountTypeForm()
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('Role for user {} successfully changed to {}.'.format(
            user.full_name(), user.role.name), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route('/user/<int:user_id>/delete')
@login_required
@admin_required
def delete_user_request(user_id):
    """Request deletion of a user's account."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/user/<int:user_id>/_delete')
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user's account."""
    if current_user.id == user_id:
        flash('You cannot delete your own account. Please ask another '
              'administrator to do this.', 'error')
    else:
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        flash('Successfully deleted user %s.' % user.full_name(), 'success')
    return redirect(url_for('admin.registered_users'))


@admin.route('/_update_editor_contents', methods=['POST'])
@login_required
@admin_required
def update_editor_contents():
    """Update the contents of an editor."""

    edit_data = request.form.get('edit_data')
    editor_name = request.form.get('editor_name')

    editor_contents = EditableHTML.query.filter_by(
        editor_name=editor_name).first()
    if editor_contents is None:
        editor_contents = EditableHTML(editor_name=editor_name)
    editor_contents.value = edit_data

    db.session.add(editor_contents)
    db.session.commit()

    return 'OK', 200

@admin.route('/userapprove', methods=['POST'])
@csrf.exempt
def userapprove():
    user_id=request.form['user_to_approve']
    user = User.query.filter_by(id=user_id).first()
    user.admin_confirmed=1
    user.update_user()
    return redirect(url_for('admin.pending_approval'))
