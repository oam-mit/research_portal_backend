from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from research_portal.settings import LOGIN_URL

def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=LOGIN_URL):

    actual_decorator = user_passes_test(
        lambda u:(u.is_active and u.is_student),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def faculty_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=LOGIN_URL):

    actual_decorator = user_passes_test(
        lambda u: (u.is_active and u.is_faculty),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator