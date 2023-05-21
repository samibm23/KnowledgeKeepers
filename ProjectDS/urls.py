"""ProjectDS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import statistics
from django.conf import settings
from django.contrib import admin
from django.urls import path
from knowledgeKeepers.views import *
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('text-to-speech/', index, name='index'),
    path('speech_to_text/', speech_to_text, name='speech_to_text'),
    path('whiteboard/', detect_text, name='whiteboard'),
    path('art/',generate_image, name="art"),
    path('MathProblem/',getText, name="Math"),
    path('GenerateImage/',GenerateImage, name="GenerateImage"),
    path('signup/',signup, name="signup"),
    path("grade_getter/",grade_getter, name="grade_getter"),
    path('save-image/',save_captured_face_view, name="Image"),
    path('ishe/',auth_page,name="auth_page"),
    path("face_capture/",face_capture, name="face_capture"),
    path('auth/',authenti, name="auth"),
    path('login/',login_view, name="login"),
    path('get_csrf_token/',get_csrf_token, name="get_csrf_token"),
    path('home/',home, name="home"),
    path('land/',land, name="land"),
    path('avatar/',avatar, name="avatar"),
    path('avatar_collection/',avatar_collection, name="collection"),
    path('show_similar_problems/', show_similar_problems, name="similarprob"),
    path('addpoints/',addpoints,name="addpoints"),
    path('students/', show_students, name="students"),
    path('grade/', pred_grade, name="grade"),
    path('historique/', hist_student, name="historique"),
    path('chooseLang/',chooseLang, name="chooseLang"),
    path('history/',history, name = "history"),
    path('test/',test_you_page, name="test"),
    path('student_email/',student_email, name="student_email"),
    path('chart/',chart, name="chart"),








]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
