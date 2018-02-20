from django.contrib import admin
from .models import *


class ShooterAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'organization', 'license_number', 'is_supervisor')
    list_filter = ('organization', 'is_supervisor')


class MatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'match_date', 'organizer')
    list_filter = ('organizer', )

    def get_form(self, request, obj=None, **kwargs):
        form = super(MatchAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['supervisor'].queryset = form.base_fields['supervisor'].queryset.filter(is_supervisor=True)
        return form


class ResultAdmin(admin.ModelAdmin):
    list_display = ('match', 'shooter', 'count')
    list_filter = ('match', 'shooter')


class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('shooter', 'match')
    list_filter = ('shooter', 'match')

admin.site.register(Organization)
admin.site.register(Match, MatchAdmin)
admin.site.register(Shooter, ShooterAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Participation, ParticipationAdmin)
