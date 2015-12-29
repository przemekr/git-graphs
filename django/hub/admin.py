from django.contrib import admin
from .models import *

admin.site.register(Project)
admin.site.register(Author)
admin.site.register(Commit)
admin.site.register(Contribution)

# Register your models here.
