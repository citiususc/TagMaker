from django.contrib import admin
from .models import Team


class TeamAdmin(admin.ModelAdmin):
    model = Team
    filter_horizontal = ('users',)


admin.site.register(Team, TeamAdmin)