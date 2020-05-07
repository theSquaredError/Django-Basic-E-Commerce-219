from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

# Register your models here.

from django.utils.html import format_html

from products.models import Category, Product, Images



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent','status')
    list_filter = ('parent', 'status')

class ImagesInline(admin.TabularInline):
    model = Images
    extra = 3

class ImagesAdmin(admin.ModelAdmin):
    fields = ['image_tag']
    readonly_fields = ['image_tag']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category','image_tag','price','amount','status')
    list_filter = ('category', 'status','price','amount')
    inlines = [ImagesInline]

    def image_tag(self, obj):
        return format_html('<img src="{}" height="30" />'.format(obj.image.url))

    image_tag.short_description = 'Image'


class ModelClass:
    ## content = models.TextField()
    detail = RichTextUploadingField()

class PostForm(forms.ModelForm):
    detail = forms.CharField(widget=CKEditorUploadingWidget())




admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)# Register your models here.
#admin.site.register(Images)