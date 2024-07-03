from django.contrib import admin
from .models import User, Posts, Follows, Likes

# Register your models here.
admin.site.register(User)
admin.site.register(Follows)
admin.site.register(Posts)
admin.site.register(Likes)
