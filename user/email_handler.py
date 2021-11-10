from verify_email.email_handler import *


class VerifyEmail:
    """
    This class does four things:
    1. creates tokens for each user.
    2. set each user as inactive and saves it
    3. embed encoded token with encoded email to make verification link.
    4. sends the email to user with that link.
    """

    def __init__(self):
        self.settings = GetFieldFromSettings()

    def __get_hashed_token(self, user):
        return urlsafe_b64encode(str(default_token_generator.make_token(user)).encode('utf-8')).decode('utf-8')

    def __make_verification_url(self, request, inactive_user, useremail):
        token = self.__get_hashed_token(inactive_user)
        email_enc = urlsafe_b64encode(
            str(useremail).encode('utf-8')).decode('utf-8')
        link = f"/verification/user/verify-email/{email_enc}/{token}/"

        absolute_link = request.build_absolute_uri(link)

        return absolute_link

    def send_verification_link(self, is_faculty, request, form):
        inactive_user = form.save(is_faculty=is_faculty)

        try:
            useremail = form.cleaned_data.get(
                self.settings.get('email_field_name'))
            if not useremail:
                raise KeyError(
                    'No key named "email" in your form. Your field should be named as email in form OR set a variable'
                    ' "EMAIL_FIELD_NAME" with the name of current field in settings.py if you want to use current name '
                    'as email field.'
                )

            verification_url = self.__make_verification_url(
                request, inactive_user, useremail)
            subject = self.settings.get('subject')
            msg = render_to_string(
                'email_verification_msg.html', {"link": verification_url})

            try:
                send_mail(subject, strip_tags(msg), from_email=self.settings.get('from_alias'),
                          recipient_list=[useremail], html_message=msg)
                return inactive_user
            except (BadHeaderError, SMTPException):
                inactive_user.delete()
                return False

        except Exception as error:

            inactive_user.delete()
            if self.settings.get('debug_settings'):
                raise Exception(error)


def send_verification_email(request, is_faculty, form):
    return VerifyEmail().send_verification_link(request=request, form=form, is_faculty=is_faculty)
