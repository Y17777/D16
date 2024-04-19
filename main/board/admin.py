from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe

from .models import Bullets, Category, Comment


class BulletsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Bullets
        fields = '__all__'


@admin.register(Bullets)
class BulletsAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'photo', 'post_photo', 'cat']
    readonly_fields = ['post_photo']
    list_display = ('title', 'post_photo', 'cat')
    list_display_links = ('title',)
    ordering = ('-dateCreation', 'title')
    list_per_page = 15
    search_fields = ['title', 'content', 'cat__name']
    list_filter = ['cat__name']
    save_on_top = True
    form = BulletsAdminForm

    @admin.display(description='Изображение', ordering='content')
    def post_photo(self, bull: Bullets):
        if bull.photo:
            return mark_safe(f"<img src='{bull.photo.url}' width=50")
        return "Нет фото"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Comment)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    list_display_links = ('id', 'text')
