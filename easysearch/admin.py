from django.contrib import admin

from .models import Department, Category, Segment, Pdf


# Register your models here.


class DepartmentAdmin(admin.ModelAdmin):
    pass
    list_display = ('DEPARTMENT',)


admin.site.register(Department, DepartmentAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass
    list_display = ('CATEGORY',)


admin.site.register(Category, CategoryAdmin)


class SegmentAdmin(admin.ModelAdmin):
    pass
    list_display = ('SEGMENT',)


admin.site.register(Segment, SegmentAdmin)


class PdfAdmin(admin.ModelAdmin):
    pass
    list_display = ('department', 'category', 'segment', 'name', 'time',)
    list_filter = ('department', 'category', 'segment', 'time',)
    ordering = ('-time',)


admin.site.register(Pdf, PdfAdmin)
