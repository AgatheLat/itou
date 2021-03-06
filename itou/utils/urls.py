from django.conf import settings
from django.utils.http import is_safe_url


def get_safe_url(request, param_name, fallback_url=None):

    url = request.GET.get(param_name) or request.POST.get(param_name)

    allowed_hosts = settings.ALLOWED_HOSTS
    require_https = request.is_secure()

    if url:

        if settings.DEBUG:
            # In DEBUG mode the network location part `127.0.0.1:8000` contains
            # a port and fails the validation of `is_safe_url` since it's not a
            # member of `allowed_hosts`:
            # https://github.com/django/django/blob/23946bd/django/utils/http.py#L393
            # As a quick fix, we build a new URL without the port.
            # pylint: disable=C0415
            from urllib.parse import urlparse, ParseResult

            url_info = urlparse(url)
            url_without_port = ParseResult(
                scheme=url_info.scheme,
                netloc=url_info.hostname,
                path=url_info.path,
                params=url_info.params,
                query=url_info.query,
                fragment=url_info.fragment,
            ).geturl()
            if is_safe_url(url_without_port, allowed_hosts, require_https):
                return url

        else:
            if is_safe_url(url, allowed_hosts, require_https):
                return url

    return fallback_url


class SiretConverter:
    """
    Custom path converter for Siret.
    https://docs.djangoproject.com/en/dev/topics/http/urls/#registering-custom-path-converters
    """

    regex = "[0-9]{14}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return f"{value}"
