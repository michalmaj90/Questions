from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from datetime import datetime
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login, logout
from .models import SCHOOL_CLASS, Student, SchoolSubject, StudentGrades, StudentNotice
from .forms import StudentSearchForm, AddStudentForm, CONVERSION, CurrencyForm, AddGradesForm, PizzaToppingsForm, TOPPINGS, PresenceListForm, BackgroundColorForm, BACKGROUND_COLOR, LoginForm, PersonalDataForm, CheckSexForm, StringNumberForm, AddSubjectForm, MessageForm, StudentNoticeForm, AddUserForm, ResetPasswordForm

# Create your views here.
class SchoolView(View):

    def get(self, request):
        html = """<!doctype html>

<html>
    <head><meta charset="utf-8"></head>
    <body>
        <h1>Szkoła podstawowa nr 1 im. Chucka Norrisa.</h1>
        <h2>Klasy:</h2>
        <ul>
            {}
        </ul>
    </body>
</html>
"""
        class_list = []
        for school_class in SCHOOL_CLASS:
            class_list.append("<li><a href='/class/{}'>{}</a></li>".format(school_class[0], school_class[1]))
        classes_part = "".join(class_list)
        return HttpResponse(html.format(classes_part))


class SchoolClassView(View):

    def get(self, request, school_class):
        students = Student.objects.filter(school_class=school_class)
        def get_class(id):
            for class_id, class_name in SCHOOL_CLASS:
                if int(id) == class_id:
                    return class_name
        return render(request, "class.html", {"students": students,
                                              "class_name": get_class(school_class)})

class StudentView(View):

    def get(self, request, student_id):
        student = Student.objects.get(pk=student_id)
        subjects = SchoolSubject.objects.all()
        def get_class(id):
            for class_id, class_name in SCHOOL_CLASS:
                if int(id) == class_id:
                    return class_name
        ctx = {
            "student": student,
            "subjects": subjects,
            "class_name": get_class(student.school_class)
        }
        return render(request, "student_info.html", ctx)

class StudentGradesView(View):

    def get(self, request, student_id, subject_id):
        student = Student.objects.get(pk=student_id)
        subject = SchoolSubject.objects.get(pk=subject_id)
        grades = StudentGrades.objects.filter(student=student, school_subject=subject)
        def get_class(id):
            for class_id, class_name in SCHOOL_CLASS:
                if int(id) == class_id:
                    return class_name
        def grades_avg():
            grade_sum = 0.0
            if len(grades) != 0:
                for grade in grades:
                    grade_sum += float(grade.grade)
                return grade_sum/len(grades)
            else:
                return "Nie dzielimy przez 0!"

        def grades_list():
            all_grades = []
            for grade in grades:
                all_grades.append(grade.grade)
            return all_grades

        ctx = {
            "student": student,
            "subject": subject,
            "class": get_class(student.school_class),
            "grades": grades_list(),
            "avg": grades_avg(),
        }
        return render(request, "student_grades.html", ctx)

class StudentSearchView(View):
    def get(self, request):
        form = StudentSearchForm()
        ctx = {
            'form': form,
        }
        return render(request, 'student_search.html', ctx)

    def post(self, request):
        form = StudentSearchForm(request.POST)
        if form.is_valid():
            last_name = form.cleaned_data['last_name']
            students = Student.objects.filter(last_name__contains = last_name)
        ctx = {
            'form': form,
            'last_name': last_name,
            'students': students,
        }
        return render(request, 'student_search.html', ctx)

class AddStudentView(View):

    def get(self, request):
        form = AddStudentForm()
        ctx = {
            'form': form,
        }
        return render(request, "add_student.html", ctx)

    def post(self, request):
        form = AddStudentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            student_class = form.cleaned_data['class_name']
            year_of_birth = form.cleaned_data['year_of_birth']
            for class_id, class_name in SCHOOL_CLASS:
                if class_name == student_class:
                    class_to_add = class_id
            new_student = Student.objects.create(first_name=first_name, last_name=last_name, school_class=class_to_add, year_of_birth=year_of_birth)
            return HttpResponseRedirect("/student/%s" %new_student.id)
        else:
            ctx = {
                'form': form,
            }
            return render(request, 'add_student.html', ctx)

class CurrencyView(View):

    def get(self, request):
        form = CurrencyForm()
        ctx = {
            'form': form,
        }
        return render(request, "currency.html", ctx)

    def post(self, request):
        form = CurrencyForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data['currency']
            conversion = form.cleaned_data['conversion']
            if conversion == 1:
                final_currency = round(currency/3.5, 2)
                return HttpResponse("%s USD" %final_currency)
            else:
                final_currency = round(currency*3.5, 2)
                return HttpResponse("%s PLN" %final_currency)

class AddGradesView(View):

    def get(self, request):
        form = AddGradesForm()
        ctx = {
            'form': form,
        }
        return render(request, 'add_grades.html', ctx)

    def post(self, request):
        form = AddGradesForm(request.POST)
        if form.is_valid():
            student_last_name = form.cleaned_data['student']
            students = Student.objects.filter(last_name=student_last_name)
            subject_name = form.cleaned_data['subject']
            subjects = SchoolSubject.objects.filter(name=subject_name)
            grade = form.cleaned_data['grade']
            if students:
                for student in students:
                    student_to_add = student
                for subject in subjects:
                    subject_to_add = subject
                StudentGrades.objects.create(student=student_to_add, school_subject=subject_to_add, grade=grade)
                return HttpResponse("Udało się!")
            else:
                return HttpResponse("Nie ma takiego ucznia!")


class PizzaToppingsView(View):
    def get(self, request):
        form = PizzaToppingsForm()
        ctx = {
            'form': form,
        }
        return render(request, 'pizza_tops.html', ctx)


class PresenceListView(View):
    def get(self, request, student_id, date):
        form = PresenceListForm()
        student = Student.objects.get(pk=student_id)
        presence_date = (datetime.strptime(date, "%Y%m%d")).date
        ctx = {
            'form': form,
            'date': presence_date,
        }
        return render(request, 'presence_list.html', ctx)

    def post(self, request, student_id, date):
        form = PresenceListForm(request.POST)
        if form.is_valid():
            student = Student.objects.get(pk=student_id)
            presence_date = (datetime.strptime(date, "%Y%m%d")).date
            present = form.cleaned_data['present']
            PresenceList.objects.create(student=student, day=presence_date, present=present)
        return HttpResponse('Dodano do listy obecności!')


class BackgroundColorView(View):

    def get(self, request):
        form = BackgroundColorForm()
        ctx = {
            'form': form,
        }
        return render(request, 'background_color.html', ctx)

    def post(self, request):
        form = BackgroundColorForm(request.POST)
        if form.is_valid():
            color = form.cleaned_data['background_color']
            ctx = {
                'form': form,
                'color': color,
            }
        return render(request, 'background_color.html', ctx)


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        ctx = {
            'form': form,
        }
        return render(request, 'login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            if login == 'root' and password == 'very\_secret':
                return HttpResponse("Miło Cię widzieć!")
            else:
                return HttpResponse("A sio wstrętny hackerze!!")


class PersonalDataView(View):

    def get(self, request):
        form = PersonalDataForm()
        ctx = {
            'form': form,
        }
        return render(request, "personal.html", ctx)

    def post(self, request):
        form = PersonalDataForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            www = form.cleaned_data['www']
            ctx = {
                'form': form,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'www': www,
            }
            return render(request, "personal_good.html", ctx)
        else:
            ctx = {
                'form': form,
            }
            return render(request, "personal.html", ctx)


class CheckSexView(View):

    def get(self, request):
        form = CheckSexForm()
        ctx = {
            'form': form,
        }
        return render(request, 'check_sex.html', ctx)

    def post(self, request):
        form = CheckSexForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            return HttpResponse("Imię: %s Nazwisko: %s" %(first_name, last_name))
        else:
            ctx = {
                'form': form,
            }
            return render(request, 'check_sex.html', ctx)


class StringNumberView(View):

    def get(self, request):
        form = StringNumberForm()
        ctx = {
            'form': form,
        }
        return render(request, 'str_num.html', ctx)

    def post(self, request):
        form = StringNumberForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data['word']
            number = int(form.cleaned_data['number'])
            return HttpResponse(("%s, " %word)*number)
        else:
            ctx = {
                'form': form,
            }
            return render(request, 'str_num.html', ctx)


class AddSubjectView(View):

    def get(self, request):
        form = AddSubjectForm()
        ctx = {
            'form': form,
        }
        return render(request, 'add_subject.html', ctx)

    def post(self, request):
        form = AddSubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Dodano przedmiot!")


class MessageView(View):

    def get(self, request):
        form = MessageForm()
        ctx = {
            'form': form,
        }
        return render(request, 'message.html', ctx)

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Wiadomość została zapisana")


class AddNoticeView(CreateView):
    template_name = 'studentnotice_form.html'
    success_url = '/add_notice/'
    model = StudentNotice
    fields = ['from_who', 'to', 'content']
    # def get(self, request):
    #     form = StudentNoticeForm()
    #     ctx = {
    #         'form': form,
    #     }
    #     return render(request, 'notice.html', ctx)
    #
    # def post(self, request):
    #     form = StudentNoticeForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponse('Dodano notatkę!')


class StudentNoticeView(View):

    def get(self, request, student_id):
        student = Student.objects.get(pk=student_id)
        notices = StudentNotice.objects.filter(to=student)
        ctx = {
            'student_id': student.id,
            'notices': notices,
        }
        return render(request, 'student_notice.html', ctx)


class DeleteNoticeView(View):

    def get(self, request, notice_id):
        notice = StudentNotice.objects.get(pk=notice_id)
        ctx = {
            'notice': notice,
        }
        notice.delete()
        return HttpResponse("Usunięto notatkę!")


class ListUsersView(View):

    def get(self, request):
        users = User.objects.all()
        ctx = {
            'users': users,
        }
        return render(request, 'list_users.html', ctx)


class LoginUserView(View):

    def get(self, request):
        form = LoginForm()
        ctx = {
            'form': form,
        }
        return render(request, 'login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                ctx = {
                    'user': user,
                }
                return render(request, 'login_user.html', ctx)
            else:
                return HttpResponse("Nie udało się sprawdzić użytkownika")


class LogoutUserView(View):

    def get(self, request):
        logout(request)
        return render(request, 'login_user.html')


class AddUserView(View):

    def get(self, request):
        form = AddUserForm()
        ctx = {
            'form': form,
        }
        return render(request, 'add_user.html', ctx)

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            users = User.objects.filter(username=username)
            password1 = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            ct = ContentType.objects.get_for_model(User)
            p = Permission.objects.get(content_type=ct, codename='change_user')
            if not users:
                if password1 != password2:
                    return HttpResponse("Podane hasła są różne")
                else:
                    user = User.objects.create_user(username=username, password=password1, first_name=first_name, last_name=last_name, email=email)
                    user.user_permissions.add(p)
                    user.save()
                    return HttpResponse("Utworzono użytkownika {}!".format(username))
            else:
                return HttpResponse("Taki użytkownik już istnieje!")
        else:
            ctx = {
                'form': form,
            }
            return render(request, 'add_user.html', ctx)


class ResetPasswordView(View):

    def get(self, request, id):
        user = User.objects.get(pk=id)
        form = ResetPasswordForm()
        ctx = {
            'form': form,
            'user': user,
            }
        def confirm_user(request):
            if request.user.has_perm('change_user'):
                return render(request, 'reset_password.html', ctx)
            else:
                return HttpResponse("Użytkownik {} nie ma uprawnień do zmiany hasła" .format(user))
        return confirm_user(request)

    def post(self, request, id):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=id)
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2:
                user.set_password(password1)
                user.save()
                return HttpResponse("Dokonano zmiany hasła!")
            else:
                return HttpResponse("Podane hasła są różne!")


class CreatePermissionView(View):
    def get(self, request):
        ct = ContentType.objects.get_for_model(User)
        p = Permission.objects.create(codename='create_user', name='Can change password', content_type=ct)
        return HttpResponse("Udało się utworzyć uprawnienie!")

class GivePermissionView(View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        ct = ContentType.objects.get_for_model(User)
        p = Permission.objects.get(content_type=ct, codename='change_user', name='Can change password')
        user.user_permissions.add(p)
        user.save()
        return HttpResponse("Nadano użytkownikowi {} uprawnienia".format(user.username))
