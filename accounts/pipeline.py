from django.utils.text import slugify
from requests import request, HTTPError
from django.core.files.base import ContentFile
from datetime import datetime


# def save_profile_picture(backend, user, response, details, is_new=False, *args, **kwargs):
#     if is_new and backend.name == "facebook":
#         url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
#         try:
#             response = request('GET', url, params={'type': 'large'})
#             response.raise_for_status()
#         except HTTPError:
#             pass
#         else:
#             profile = kwargs.get("profile")
#             if profile:
#                 profile.photo.save(u'{0}_social.jpg'.format(slugify(user.username)), ContentFile(response.content))
#                 profile.save()


def save_extra_data(backend, user, response, details, is_new=False, *args, **kwargs):
    if is_new and backend.name == "facebook":
        genders = {"male": "m", "female": "f"}
        gender = response.get('gender')
        gender = genders.get(gender, "")
        user.gender = gender
        user.save()
        return {"user": user}
