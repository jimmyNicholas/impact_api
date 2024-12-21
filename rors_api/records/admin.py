from django.contrib import admin
from django.db.models import Avg
from .models import (
    Teacher, 
    Course, 
    Class, 
    Student,
    NumericAssessment,
    GradedAssessment
)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_name_display', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'start_date', 'end_date', 'is_active')
    list_filter = ('course', 'is_active')
    search_fields = ('name',)
    filter_horizontal = ('teachers',)
    date_hierarchy = 'start_date'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id', 
        'first_name', 
        'last_name', 
        'nickname', 
        'current_class',
        'start_date', 
        'is_active'
    )
    list_filter = ('current_class', 'is_active')
    search_fields = (
        'student_id', 
        'first_name', 
        'last_name', 
        'nickname'
    )
    date_hierarchy = 'start_date'
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'student_id', 
                'first_name', 
                'last_name', 
                'nickname'
            )
        }),
        ('Class Information', {
            'fields': (
                'current_class',
                'start_date',
                'is_active'
            )
        }),
        ('Additional Information', {
            'fields': (
                'participation',
                'teacher_comments'
            )
        }),
    )

@admin.register(NumericAssessment)
class NumericAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        'student', 
        'skill', 
        'week', 
        'score', 
        'status',
        'submission_date'
    )
    list_filter = (
        'skill', 
        'status', 
        'week',
        'submission_date'
    )
    search_fields = (
        'student__first_name', 
        'student__last_name', 
        'student__student_id'
    )
    date_hierarchy = 'submission_date'
    readonly_fields = ('score',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student')

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'COM': 
            return self.readonly_fields + ('correct_answers', 'total_questions')
        return self.readonly_fields

@admin.register(GradedAssessment)
class GradedAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        'student', 
        'skill', 
        'week', 
        'grade', 
        'status',
        'submission_date'
    )
    list_filter = (
        'skill', 
        'status', 
        'grade', 
        'week',
        'submission_date'
    )
    search_fields = (
        'student__first_name', 
        'student__last_name', 
        'student__student_id', 
        'comments'
    )
    date_hierarchy = 'submission_date'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student')

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'COM':
            return ('grade',)
        return ()
