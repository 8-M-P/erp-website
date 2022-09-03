from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls'), name='core'),
    path('api/', include('api.urls'), name='api'),
    path('front-end/', include('front_end.urls'), name='front-end'),
    path('__debug__/', include('debug_toolbar.urls')),

]
