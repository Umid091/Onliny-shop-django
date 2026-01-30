from django.contrib import admin


from .models import Product,Category ,ProductImage

admin.site.register([Product,Category,ProductImage])

