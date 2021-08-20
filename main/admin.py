from django.contrib import admin

from .models import Submission, Problem


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at')
    readonly_fields = ('id', 'problem', 'code', 'status', 'created_at')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
