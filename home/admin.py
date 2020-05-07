from django.contrib import admin

# Register your models here.
from home.models import Contact, Comment


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','subject','status','create_at')
    list_filter = ('status','create_at')
    readonly_fields = ('name', 'email','subject','message')

admin.site.site_title = "Summer Project Admin Panel"
admin.site.site_header = "Summer Project Admin Panel"
admin.site.index_title = "Summer Project Admin Panel Home"

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','product','subject','message','rating','status','create_at')
    list_filter = ('status','create_at')
    readonly_fields = ('product','user','subject','message','rating')
    list_display_links = ('subject','product',)
    list_editable = ('status',)


admin.site.register(Contact,ContactAdmin)
admin.site.register(Comment,CommentAdmin)