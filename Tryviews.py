
@login_required
def student_dashboard(request):
    # Ensure we're fetching the correct logged-in student's details
    student = request.user  # Logged-in student

    if student.user_type != 'student':
        return render(request, 'error.html', {'message': 'Unauthorized access'})  # Ensure only students can access this dashboard

    # Get the list of teachers assigned to the logged-in student (via accepted requests)
    student_requests = TeacherRequest.objects.filter(student=student, status='accepted')
    teachers = [request.teacher for request in student_requests]  # Get a list of teachers who have been accepted

    class_schedules = ClassSchedule.objects.filter(student=student)

    if request.method == 'POST':
        form = ProposeTimeForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.student = student
            teacher_id = request.POST.get('teacher')  # Get the teacher from the form
            if teacher_id:
                schedule.teacher = CustomUser.objects.get(id=teacher_id)  # Assign the teacher
            schedule.save()
            return redirect('student_dashboard')
    else:
        form = ProposeTimeForm()

    return render(request, 'accounts/student_dashboard.html', {
        'teachers': teachers,  # Pass the teachers list to the template
        'student': student,  # Pass the student object to display correct username
        'class_schedules': class_schedules,
        'form': form,
    })



# views.py
@login_required
def search_teachers(request):
    if request.method == 'GET':
        district = request.GET.get('district')
        medium = request.GET.get('medium')
        subject = request.GET.get('subject')
        
        # Filter based on search criteria
        teachers = CustomUser.objects.filter(user_type='teacher', district=district, medium=medium, subject=subject, is_active=True)
        
        context = {
            'teachers': teachers
        }
        return render(request, 'accounts/search_teachers.html', context)
    