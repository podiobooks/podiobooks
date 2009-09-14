from django.conf.urls.defaults import patterns, url
from models import Category, Title

urlpatterns = patterns('',
    
    # title
    url(r'^title/$','django.views.generic.list_detail.object_list', { 'queryset': Title.objects.all().order_by('name'), 'template_object_name': 'title', 'template_name': 'main/title/list.html'}, 'title_list'),
    url(r'^title/(?P<slug>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Title.objects.all(), 'template_object_name': 'title', 'template_name': 'main/title/detail.html'}, 'title_detail'),

    # category
    url(r'^category/$','django.views.generic.list_detail.object_list', { 'queryset': Category.objects.all().order_by('name'), 'template_object_name': 'category', 'template_name': 'main/category/list.html'}, 'category_list'),
    url(r'^category/(?P<slug>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Category.objects.all(), 'template_object_name': 'category', 'template_name': 'main/category/detail.html'}, 'category_detail'),
    
    # Browse Category Redirect
    url(r'^browsecategory/$', 'pbsite.main.views.browse_category', name="browse_category"),
                       
)
