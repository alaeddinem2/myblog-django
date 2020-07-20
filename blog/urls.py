from django.urls import path

from . import views

urlpatterns=[
path('',views.home,name='home'),
path('about/',views.about,name='about'),
path('project/',views.project,name='project'),
path('detail/<int:post_id>/',views.post_detail,name='detail'),
path('new_post/',views.PostCreateView.as_view(),name='new_post'),
path('detail/<slug:pk>/update',views.PostUpdateView.as_view(),name='post_update'),
path('detail/<slug:pk>/delete',views.PostDeleteView.as_view(),name='post_delete'),
path('weather/',views.weather,name='weather'),
path('delete_comment/<int:post_id>',views.delete_comment,name='delete_comment'),
path('like/<int:pk>',views.LikeView,name='like_post'),
path('hitcount/', views.get_view_data, name='hitcount'),
path('category/<str:cats>/',views.category_view,name='category')



]