from django.urls import path
from bluebird import views


urlpatterns = [
    path('contragents/', views.ContragentsView.as_view()),
    path('tasks/<str:group_id>', views.TasksView.as_view()),
]
