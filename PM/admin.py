from django.contrib import admin
from .models import GA


class GAAdmin(admin.ModelAdmin):

    list_display = ('generation', 'popularity')


admin.site.register(GA, GAAdmin)
