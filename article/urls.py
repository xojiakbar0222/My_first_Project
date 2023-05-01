from .views import list_view, index, new, detail_view, post_share, categories_list
from django.urls import path



app_name = 'article'

urlpatterns = [
    path('category/<int:id>/', categories_list, name = 'catogories_list'),
    path('<int:id>/', detail_view, name='detail'),
    path('<int:id>/share/', post_share, name='share'),
    path('', list_view, name='list')
    # path('', index),
    # path('news', new)


]

