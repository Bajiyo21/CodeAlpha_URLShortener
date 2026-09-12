import json
import random
import string

from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.template.response import TemplateResponse
import qrcode

from .models import UrlMapping


def home(request):
    return TemplateResponse(request, 'index.html')


def history(request):
    total_urls = UrlMapping.objects.count()
    total_clicks = sum(item.clicks for item in UrlMapping.objects.all())
    active_links = UrlMapping.objects.count()
    urls = UrlMapping.objects.all().order_by('-created_at')
    return TemplateResponse(request, 'history.html', {
        'total_urls': total_urls,
        'total_clicks': total_clicks,
        'active_links': active_links,
        'urls': urls,
    })


@require_http_methods(['POST'])
def shorten_url(request):
    body = json.loads(request.body)
    original_url = body.get('original_url', '').strip()
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url

    short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    while UrlMapping.objects.filter(short_code=short_code).exists():
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    mapping = UrlMapping.objects.create(original_url=original_url, short_code=short_code)

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(original_url)
    qr.make(fit=True)
    image = qr.make_image(fill_color='black', back_color='white')

    qr_name = f'qr_codes/{short_code}.png'
    img_buffer = settings.BASE_DIR / 'media' / qr_name
    # On local disk, create a file in media folder.
    img_buffer.parent.mkdir(parents=True, exist_ok=True)
    image.save(img_buffer)

    short_url = request.build_absolute_uri('/') + short_code + '/'
    return JsonResponse({
        'short_url': short_url,
        'qr_code': '/media/' + qr_name,
        'original_url': original_url,
    })


@require_http_methods(['GET'])
def url_history(request):
    urls = list(UrlMapping.objects.values('id', 'original_url', 'short_code', 'created_at', 'clicks'))
    return JsonResponse({'urls': urls})


def redirect_url(request, short_code):
    mapping = get_object_or_404(UrlMapping, short_code=short_code)
    mapping.clicks += 1
    mapping.save(update_fields=['clicks'])
    return HttpResponseRedirect(mapping.original_url)
