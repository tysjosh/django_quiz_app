from django.shortcuts import render, redirect, reverse
from django.http import Http404, HttpResponse
from django.contrib import messages
from .models import UserProfile, Category, Quiz, QuizResult, Question
from .form import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

#using class based views for quizzes
#one way of creating class based view
#Quiz CRUD
class QuizListView(ListView):
    model = Quiz
    template_name = "quiz/quiz.html"
    context_object_name = 'quizzes'
    ordering= ['-creation_date']


#another way of creating class based view without assigning template_name and context_object_name
class QuizDetailView(DetailView):
    model = Quiz

class QuizResultView(DetailView):
    model = QuizResult
    template_name = "quiz/quiz_result.html"
    context_object_name = 'quiz_result'

#using PermissionRequiredMixin to make sure user are logged in and have permission
#before they can navigate to this view
class QuizCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ['quiz.add_quiz']
    model = Quiz
    fields = ['title', 'description', 'category', 'region', 'active']
    
class QuizUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ['quiz.change_quiz']
    model = Quiz
    fields = ['title', 'description', 'category', 'region', 'active']
    
class QuizDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ['quiz.delete_quiz']
    model = Quiz
    success_url = '/'

#Category CRUD
class CategoryListView(ListView):
    model = Category
    template_name = "quiz/category.html"
    context_object_name = 'categories'

class CategoryCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ['quiz.add_category']
    model = Category
    fields = ['name']
    success_url = '/'

class CategoryUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ['quiz.change_category']
    model = Category
    fields = ['name']
    success_url = '/'

class CategoryDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ['quiz.delete_category']
    model = Category
    success_url = '/'


class QuizResultsListView(ListView):
    model = QuizResult
    template_name = "quiz/quizresults.html"
    context_object_name = 'quizresults'
    
#Question CRUD
@login_required
def perform_quiz(request, pk):

    if request.method == "GET":
        questions = Question.objects.filter(quiz__pk=pk)
        quiz = Quiz.objects.filter(pk=pk).first()

        return render(request, 'quiz/questions.html', {
        'questions': questions,
        'quiz': quiz
        })

    if request.method == "POST":
        questions = Question.objects.filter(quiz__pk=pk)
        quiz = Quiz.objects.filter(pk=pk).first()
        user_profile = UserProfile.objects.filter(user=request.user).first()

        score = 0

        for question in questions:
            user_ans = request.POST.get(str(question.pk))
            if user_ans == question.correct_answer:
                score += 1

        quiz_result = QuizResult.objects.create(quiz=quiz,user_profile=user_profile,score=score)
        quiz_result.save()

        return render(request, 'quiz/quiz_finish.html', {
            'quiz_result': quiz_result,
         })

class QuestionListView(TemplateView):
    template_name = "question.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = Quiz.objects.get(id=quiz.id)

        context['questions'] = Question.objects.filter(quiz = quiz)
        return context


class QuizQuestionsListView(TemplateView):
    template_name = "quiz/quiz_questions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz_id = kwargs["pk"]
        quiz = Quiz.objects.get(id=quiz_id)

        context['questions'] = Question.objects.filter(quiz = quiz)
        context['quiz'] =quiz
        return context

class QuestionCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ['quiz.add_question']
    model = Question
    fields = ['prompt', 'quiz', 'answer_a', 'answer_b', 'answer_c', 'correct_answer']
    success_url = '/'

class QuestionUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ['quiz.change_question']
    model = Question
    fields = ['prompt', 'quiz', 'answer_a', 'answer_b', 'answer_c', 'correct_answer']
    success_url = '/'

class QuestionDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ['quiz.delete_question']
    model = Question
    success_url = '/'
    
#decided to use function based views for users
# def users(request):
#     users = UserProfile.objects.all()
#     return render(request, 'users/users.html', {
#         'users': users
#     })

def about(request):
    return render(request, 'quiz/about.html', {
        'title': 'About'
    })

# def user_detail(request, user_id):
#     try:
#         user = UserProfile.objects.get(user_id = user_id)
#     except UserProfile.DoesNotExist:
#         raise Http404("user not found")

#     return render(request, 'users/user_detail.html', {
#         'user': user
#     })

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

#making user is logged in before navigating to the view in function based view
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)
        
    return render(request, 'users/user_detail.html', {
        'u_form': u_form,
        'p_form': p_form
    })