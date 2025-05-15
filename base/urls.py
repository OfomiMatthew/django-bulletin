from django.urls import path

from . import views 

urlpatterns = [
    path('',views.index,name='index'),
    path('<slug:post_slug>/',views.PostDetails,name='bulletins'),
    path('contact',views.ContactView,name='contact'),
    path('contact-success',views.ContactSuccess,name='contact-success'),
    path('posts',views.CreatePost,name='posts'),
    path('<slug:post_slug>/create/',views.create_comment,name='create-comment'),
    path('<int:comment_id>/update/',views.update_comment,name='update-comment'),
    path('<int:comment_id>/delete/',views.delete_comment,name='delete-comment'),

    # path('search-posts',views.search_post,name='search-post'),
  
]
