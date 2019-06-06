from django.contrib import admin
from .models import Team


class TeamAdmin(admin.ModelAdmin):
    model = Team
    filter_horizontal = ('users',)  # If you don't specify this, you will get a multiple select widget.


admin.site.register(Team, TeamAdmin)