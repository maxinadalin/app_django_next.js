
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    
    # MODELS BLOG
    path("api/category/",include("apps.blog.urls")),
    
    
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
