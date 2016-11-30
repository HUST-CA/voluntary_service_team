from django.contrib import admin

from .models import ServiceObject, SMS_Feedback
from django.contrib.auth.models import Group, User


def make_complete(modeladmin, request, queryset):
    queryset.update(flag='完成')


make_complete.short_description = "把选中的ServiceObject的flag改为 完成 "


def make_done(modeladmin, request, queryset):
    queryset.update(flag='已取回')


make_done.short_description = "把选中的ServiceObject的flag改为 已取回 "


class SMSFeedbackInline(admin.TabularInline):
    model = SMS_Feedback
    extra = 1


class ServiceObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'tel', 'flag', 'trouble', 'serial_number', 'short_link')
    list_filter = ('flag', 'service_activity')
    fieldsets = (
        ('个人信息', {'fields': ('name', 'tel', 'computer_model', 'problem')}),
        ('后台记录', {'fields': ('short_link', 'service_activity')}),
        ('状态', {'fields': ('flag', 'trouble')}),
    )
    search_fields = ('name', 'tel')
    filter_horizontal = ()
    actions = [make_complete, make_done]
    inlines = [SMSFeedbackInline, ]


admin.site.register(ServiceObject, ServiceObjectAdmin)
admin.site.unregister(Group)
admin.site.unregister(User)
