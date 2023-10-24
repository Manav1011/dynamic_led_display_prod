from django.contrib.auth.signals import user_logged_in, user_logged_out
import logging

logger = logging.getLogger(__name__)

def login_logger(sender, request, user, **kwargs):
    logger.info(f'User {user.username} logged in from IP {request.META["REMOTE_ADDR"]}')

def logout_logger(sender, request, user, **kwargs):
    logger.info(f'User {user.username} logged out from IP {request.META["REMOTE_ADDR"]}')

user_logged_in.connect(login_logger)
user_logged_out.connect(logout_logger)