from django.contrib import admin

# Register your models here.

from .models import Course, Enrollment, Announcement, Comment, Lesson, Material

class CourseAdmin(admin.ModelAdmin):
    
    list_display = ['name', 'slug', 'start_date', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = { 'slug':['name']}


class MaterialInlineAdmin(admin.TabularInline):
                                # or StackedInline
    model = Material


class LessonAdmin(admin.ModelAdmin):
    
    list_display = ['name', 'number', 'course']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

    inlines = [
        MaterialInlineAdmin
    ]
admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment])
admin.site.register(Lesson, LessonAdmin)