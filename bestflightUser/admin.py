from django.contrib import admin
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin

from bestflightUser.models import User, Profile


def get_photo(obj):
    if obj.photo:
        media_url = settings.MEDIA_URL
        host = settings.DOMAIN
        url = '{}{}{}'.format(host, media_url, obj.photo)
        image = u"<img src=\"{}\" alt=\"{}profile photo\" style=\"width:5em;\"/>".format(  # noqa
            url, obj.user.first_name)
        return mark_safe(image)
    return '--'


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0
    fields = ('id', 'international_passport_number', 'picture')
    readonly_fields = fields

    def picture(self, obj):
        return get_photo(obj)


@admin.register(User)
class _UserAdmin(UserAdmin):
    inlines = [
        ProfileInline,
    ]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'international_passport_number',
        'create_date', 'picture')
    raw_id_fields = ['user']
    readonly_fields = ('create_date', 'modify_date', 'picture')
    search_fields = ['user', 'international_passport_number']

    def picture(self, obj):
        return get_photo(obj)

    def get_queryset(self, request):
        return super(ProfileAdmin, self).get_queryset(
            request).order_by('-create_date')
