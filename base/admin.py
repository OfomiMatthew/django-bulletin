from django.contrib import admin

from .models import Post,Category,Tag,Contact,Comment


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    list_filter = ["category", "status","publication_date"]
    list_display = ["title", "author","publication_date"]
    
admin.site.register(Post,PostAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    
admin.site.register(Category,CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    
admin.site.register(Tag,TagAdmin)
admin.site.register(Contact)
admin.site.register(Comment)


