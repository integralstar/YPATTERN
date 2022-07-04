from django.contrib import admin
from .models import A3C


class A3CAdmin(admin.ModelAdmin):
    list_display = ('emulator',)


admin.site.register(A3C, A3CAdmin)
