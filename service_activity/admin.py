from django.contrib import admin

from .models import ServiceActivity, Member


class ServiceActivityAdmin(admin.ModelAdmin):
    list_filter = ('flag',)
    fieldsets = (
        ('信息', {'fields': ('place', 'int_id',)}),
        ('成员', {'fields': ('members',)}),
        ('状态', {'fields': ('flag',)}),
    )
    search_fields = ('place', 'members')
    filter_horizontal = ()


class MemberAdmin(admin.ModelAdmin):
    list_filter = ('sex',)
    fieldsets = (
        ('信息', {'fields': ('name', 'sex', 'college', 'info',)}),
        ('联系方式', {'fields': ('tel', 'email',)}),
    )
    search_fields = ('name', 'college')
    filter_horizontal = ()


admin.site.register(ServiceActivity, ServiceActivityAdmin)
admin.site.register(Member, MemberAdmin)

admin.site.site_header = '义务维修队'
admin.site.site_title = '义务维修队'
