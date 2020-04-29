from django.urls import path, include

from . import views

urlpatterns = [
    path('auth/', include('apps.auth.urls')),

    path('user/my/details/', views.LoggedInUserDetailView.as_view()),
    path('user/my/ping/', views.UserPingView.as_view()),  # update 'last_action_dt'
    path('user/<int:pk>/details/', views.UserDetailView.as_view()),
    path('user/list/', views.UserListView.as_view()),

    path('rooms/', views.RoomListCreateView.as_view()),
    path('rooms/<int:pk>/', views.RoomRetrieveUpdateView.as_view()),
    path('rooms/<int:room_pk>/messages/', views.MessageListCreateView.as_view()),
]
