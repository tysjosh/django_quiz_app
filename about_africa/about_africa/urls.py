from django.contrib import admin
from django.urls import path
from quiz import views
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    #url pattern for user
    path('admin/', admin.site.urls),
    #path('users/', views.users, name='users'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    #path('user_detail/<int:user_id>', views.user_detail, name='user_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    # url pattern for quiz
    path('', views.QuizListView.as_view(), name='quiz-home'),
    path('quiz/<int:pk>/', views.QuizDetailView.as_view(), name='quiz-detail'),
    path('quiz/<int:pk>/answer/result', views.QuizResultView.as_view(), name='quiz_result'),
    path('quiz/new/', views.QuizCreateView.as_view(), name='quiz-create'),
    path('quiz/<int:pk>/update', views.QuizUpdateView.as_view(), name='quiz-update'),
    path('quiz/<int:pk>/delete', views.QuizDeleteView.as_view(), name='quiz-delete'),
    path('quiz/<int:pk>/answer', views.perform_quiz, name='quiz-perform'),
    path('quiz/<int:pk>/questions', views.QuizQuestionsListView.as_view(), name='quiz-questions'),

    #url pattern for category
    path('category/', views.CategoryListView.as_view(), name='category-list'),
    path('category/new/', views.CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/update', views.CategoryUpdateView.as_view(), name='category-update'),
    path('category/<int:pk>/delete', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('quizresults/', views.QuizResultsListView.as_view(), name='quiz_result'),

    #url pattern for Question
    #path('question/', views.QuestionListView.as_view(), name='question-list'),
    path('question/new/', views.QuestionCreateView.as_view(), name='question-create'),
    path('question/<int:pk>/update', views.QuestionUpdateView.as_view(), name='question-update'),
    path('question/<int:pk>/delete', views.QuestionDeleteView.as_view(), name='question-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)