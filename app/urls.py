from django.urls import path

from .views import *
from .api.group import GroupListView
from .api.lessons import GroupLessonsView
from .api.lesson_schedule import ScheduleView, ScheduleListView

apipatterns = [
    path('api/group/', GroupListView.as_view(), name='api-groups'),
    path('api/group/lessons/', GroupLessonsView.as_view(), name='api-group-lessons'),
    path('api/schedules/', ScheduleListView.as_view(), name='api-schedules'),
    path('api/schedules/<int:schedule_id>/', ScheduleView.as_view(), name='api-schedule-show'),
]

urlpatterns = [
    path('', index, name='main'),
    path('schedules/', shedules, name='schedules'),
    path('schedules/<int:schedule_id>/', show_schedule, name='show_schedule')
] + apipatterns
