from django.core.urlresolvers import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User

def extract_user_field(model):
    for field in model._meta.fields + model._meta.many_to_many:
        if field.rel and field.rel.to == User:
            return field.name
    for rel in model._meta.get_all_related_many_to_many_objects():
        if rel.model == User:
            return rel.var_name

def positive_filter(qs, user_qs, user_lookup=None):
    if not user_lookup:
        user_lookup = extract_user_field(qs.model)

    if not user_lookup:
        return qs.none() # default to returning none

    query = {'%s__in' % user_lookup: user_qs}

    qs = qs.filter(**query).distinct()
    return qs

def negative_filter(qs, user_qs, user_lookup=None):
    if not user_lookup:
        user_lookup = extract_user_field(qs.model)

    if not user_lookup:
        return qs # default to returning all

    query = {'%s__in' % user_lookup: user_qs}

    qs = qs.exclude(**query).distinct()
    return qs

def default_redirect(request, redirect_field_name=REDIRECT_FIELD_NAME,
        urlname=None, default=None):
    """
    Returns the URL to be used in relationship handler by looking at different
    values in the following order:

    - The URL under with the name "relationship_list_base"
    - a REQUEST value, GET or POST, named "next" by default.
    """
    if urlname:
        default_redirect_to = reverse(urlname)
    else:
        default_redirect_to = default
    redirect_to = request.REQUEST.get(redirect_field_name)
    # light security check -- make sure redirect_to isn't garabage.
    if not redirect_to or "://" in redirect_to or " " in redirect_to:
        redirect_to = default_redirect_to
    return redirect_to
