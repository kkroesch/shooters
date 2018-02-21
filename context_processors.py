from django.conf import settings

def menu(request):
    return {'menu': settings.MENU_ITEMS}