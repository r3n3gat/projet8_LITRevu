from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('',                               views.feed,               name='feed'),
    path('posts/',                         views.ticket_list,        name='ticket_list'),
    path('ticket/add/',                    views.ticket_create,      name='ticket_add'),
    path('ticket/<int:pk>/edit/',          views.ticket_edit,        name='ticket_edit'),
    path('ticket/<int:pk>/delete/',        views.ticket_delete,      name='ticket_delete'),
    path('ticket/<int:ticket_pk>/review/', views.review_create,      name='review_create'),
    path('review/add/',                    views.free_review_create, name='review_free_create'),
    path('review/<int:pk>/',               views.ReviewDetailView.as_view(),  name='review_detail'),
    path('review/<int:pk>/edit/',          views.review_edit,        name='review_edit'),
    path('review/<int:pk>/delete/',        views.review_delete,      name='review_delete'),
    path('review/<int:pk>/comment/',       views.CommentCreateView.as_view(), name='comment_create'),
    path('follows/',                       views.follow_list,        name='follow_list'),
    path('follows/add/',                   views.follow_add,         name='follow_add'),
    path('follows/<int:pk>/delete/',       views.follow_delete,      name='follow_delete'),
]
