from django.contrib import admin
from .models import Complaint
from django.contrib.auth.models import User


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):

    # list view
    list_display = (
        'id',
        'user',
        'category',
        'priority',
        'status',
        'created_at',
    )

    list_filter = ('status', 'priority', 'category')
    search_fields = ('category', 'description', 'user__username')

    # ONLY fields that must be read-only
    readonly_fields = (
        'user',
        'category',
        'description',
        'priority',
        'before_image',
        'created_at',
    )

    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Complaint Details (Read Only)', {
            'fields': ('category', 'description', 'priority')
        }),
        ('Admin Action', {
            'fields': ('status', 'after_image', 'admin_comment')
        }),
        ('Before Image', {
            'fields': ('before_image',)
        }),
        ('System Info', {
            'fields': ('created_at',)
        }),
    )

    # ❌ no adding complaints
    def has_add_permission(self, request):
        return False

    # ❌ no deleting complaints
    def has_delete_permission(self, request, obj=None):
        return False

    # ✅ allow editing (needed for status & image)
    def has_change_permission(self, request, obj=None):
        return True


# ---------------- USER: READ ONLY ---------------- #

class ReadOnlyUserAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in User._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True


admin.site.unregister(User)
admin.site.register(User, ReadOnlyUserAdmin)
