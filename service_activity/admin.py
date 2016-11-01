from django.contrib import admin

from .models import ServiceActivity


class ServiceActivityAdmin(admin.ModelAdmin):
    list_filter = ('flag',)
    fieldsets = (
        ('信息', {'fields': ('activity_date', 'place', 'int_id', 'problem')}),
        ('成员', {'fields': ('members',)}),
        ('状态', {'fields': ('flag',)}),
    )
    search_fields = ('place', 'members')
    filter_horizontal = ()


admin.site.register(ServiceActivity, ServiceActivityAdmin)
