import app.enums as enum
from flask import render_template
from app.main.views import main


@main.app_errorhandler(403)
def forbidden(_):
    return render_template('errors/403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    if e.description == enum.Errors.TICKER_NOT_FOUND.name:
        return render_template('errors/ticker_not_found.html', ticker=e.response), 404
    return render_template('errors/404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(_):
    return render_template('errors/500.html'), 500


# @main.app_errorhandler(600)
# def ticker_not_found(ticker):
#     return render_template('errors/600.html', ticker=ticker), 600
