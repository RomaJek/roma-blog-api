from django.contrib import admin
from .models import Post, Category


# Register your models here.




# 1-usil
# admin.site.register(Post)

# 2-usil
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
