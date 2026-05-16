from django.urls import path

from . import views

resources = [
    ('farmers', views.FarmerListView, views.FarmerDetailView),
    ('collectors', views.CollectorListView, views.CollectorDetailView),
    ('clerks', views.ClerkListView, views.ClerkDetailView),
    ('admins', views.AdminListView, views.AdminDetailView)
]

urlpatterns = [
    path('api/register/<str:user_type>/', views.RegisterView.as_view(), name='register'),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/logout/', views.LogoutView.as_view(), name='logout'),
]

for resource, list_view, detail_view in resources:
    urlpatterns += [
        path(f'api/{resource}/', list_view.as_view(), name=f'{resource}-list'),
        path(f'api/{resource}/<int:pk>/', detail_view.as_view(), name=f'{resource}-detail')
    ]