from django.contrib import admin
from .models import URL, Checker, ScanMode


class CheckerAdmin(admin.ModelAdmin):
    list_display = ('owner', 'content_saved', 'content_now',
                    'status_saved', 'status_now', 'page_excepted', 'last_checked', 'fixed')
    search_fields = ['owner', 'content_saved', 'content_now',
                     'status_saved', 'status_now', 'page_excepted', 'last_checked', 'fixed']


class URLAdmin(admin.ModelAdmin):
    list_display = ['url']


class ScanModeAdmin(admin.ModelAdmin):
    list_display = ['scan_mode']


admin.site.register(Checker, CheckerAdmin)
admin.site.register(URL, URLAdmin)
admin.site.register(ScanMode, ScanModeAdmin)
