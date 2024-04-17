from django.urls import path
from . import views


urlpatterns = [
    path('', views.BulletsHome.as_view(), name='home'),  # http://127.0.0.1:8000
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<int:pk>/', views.ShowPosts.as_view(), name='post'),
    path('mypost/<int:pk>/', views.ShowUserPosts.as_view(), name='post_user'),
    path('comments/<int:post_pk>/', views.ShowPostComments.as_view(), name='post_comments'),
    path('<int:pk>/addcomment/', views.CreateComment.as_view(), name='add_comment'),
    path('<int:pk>/acceptcomment/', views.accept_comment, name='accept_comment'),
    path('category/<int:pk>/', views.BulletsCategory.as_view(), name='category'),
    path('<int:pk>/edit/', views.EditPage.as_view(), name='edit_page'),
    path('<int:pk>/delete/', views.DeletePage.as_view(), name='delete_page'),
    path('<int:pk>/delcomment/', views.DeleteComment.as_view(), name='delete_comment'),
]
