from django.urls import path
from project.views import generate_collage, new_subject, get_subject_history

urlpatterns= [
    path('', generate_collage, name='generate_collage'),
    path('new-subject/', new_subject, name='new_subject'),
    path('get-subject-history/<int:subject_id>/', get_subject_history, name='get_subject_history'),
]