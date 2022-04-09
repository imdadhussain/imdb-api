from django.conf import settings


def get_media_url(request, image_path):
    media_url = None
    if request and image_path:
        media_url = f'{request.META.get("HTTP_HOST")}{settings.MEDIA_URL}{image_path}'
    return media_url
