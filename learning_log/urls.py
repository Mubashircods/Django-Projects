"""Define URL patern for learning_log"""
from django.urls import path

from . import views

app_name = 'learning_log'
urlpatterns = [
    path('', views.index, name='index'),
    path('topic/', views.topic, name='topic'),
    path('topics/<int:topic_id>', views.topics, name='topics'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>', views.edit_entry, name='edit_entry'),
]