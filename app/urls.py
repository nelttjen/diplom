from django.urls import path

from .views import *
from .api.group import GroupListView
from .api.lessons import GroupLessonsView

apipatterns = [
    path('api/group/', GroupListView.as_view(), name='api-groups'),
    path('api/group/lessons/', GroupLessonsView.as_view(), name='api-group-lessons'),
]

urlpatterns = [
    path('', index, name='main')
] + apipatterns
