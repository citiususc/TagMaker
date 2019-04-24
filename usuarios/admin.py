from django.contrib import admin
from .models import Equipo


class EquipoAdmin(admin.ModelAdmin):
    model = Equipo
    filter_horizontal = ('users',)  # If you don't specify this, you will get a multiple select widget.


admin.site.register(Equipo, EquipoAdmin)