import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView

from .Department import Department, Team
from .EmployeeSchedule import EmployeeSchedule
from .calendar import EmployeeCalendar
from .forms import EmployeeForm, DepartmentForm, TeamFormAdd, TeamForm
from .models import Employee
import pandas as pd
import cvxpy as cp
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import linprog
from pulp import *
import csv, io

#from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe


# Create your views here.
def login(request):
    return render(request, 'login.html')

def HR_Profile(request):
    return  render(request, 'hrProfile.html')

def employeeProfile(request):
    return  render(request, 'employeeProfile.html')

def schedule(request):
    return  render(request, 'schedule.html')
def timeslot(request):
    return  render(request, 'timeslot.html')
def changeSchedule(request):
    return  render(request, 'changeSchedule.html')

def calander(request):
    data = Employee.objects.all()
    return  render(request, 'calander.html', {"employees":data})

#@login_required(login_url='login')

def employeeDetails(request):
    form = EmployeeForm()  # Initialize the form variable
    if request.method == "POST":
        if 'file' in request.FILES:
            # handle CSV file upload
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a CSV file.')
            else:
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string)
                for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                    emp_data = {
                        "Emp_Id": column[0],
                        "Name": column[1],
                        "Scheduling": column[2],
                        "Department": column[3],
                        "Team": column[4],
                        "Manager_Name": column[5],
                        "Manager_Id": column[6],
                        "Email": column[7],
                    }
                    # Create a new Employee object or update the existing one
                    employee, created = Employee.objects.update_or_create(
                        Emp_Id=emp_data["Emp_Id"],
                        defaults=emp_data
                    )
                    if created:
                        # Save the newly created object
                        messages.success(request, f'Employee {employee.Emp_Id} ({employee.first_name}) created successfully.')
                    else:
                        # Save the updated object
                        messages.success(request, f'Employee {employee.Emp_Id} ({employee.first_name}) updated successfully.')
        else:
            # handle manual employee form submission
            form = EmployeeForm(request.POST)
            if form.is_valid():
                employee = form.save(commit=False)
                employee.save()
                #messages.success(request, f'Employee {employee.Emp_Id} ({employee.first_name}) saved successfully.')
                return redirect("organization")
            else:
                messages.error(request, 'Form data is not valid. Please correct the errors.')
    template = "employeeDetails.html"
    data = Employee.objects.all()
    prompt = {
        'order': 'Order of the CSV should be Emp_Id, Name, Scheduling, Department, Team, Manager_Name, Manager_Id, Email',
        'employees': data
    }
    return render(request, template, {"form": form, "prompt": prompt})
def upload(request):
    #df_r = pd.read_csv(r"account\\templates\\out.csv")
    template = "upload.html"

    if request.method == "POST":
        if 'file' in request.FILES:
            # handle CSV file upload
            print(request.FILES['file'])
            df_r,s = run_model(request.FILES['file'])


            #one_entry = Employee.objects.get(Emp_Id=1009)
            #emp_sch = EmployeeSchedule(Emp_Id=one_entry, schedule_date=datetime.date.today(), working_status='O', seat_no='A113')
            #emp_sch.save()
#
            #print(emp_sch.schedule_date.today().day)

           # form = EmployeeForm()
            tmp = df_r.to_html()
    
            json_records = df_r.reset_index().to_json(orient ='records')
            data = []
            data = json.loads(json_records)

        
            total_employees_per_day = df_r.sum(axis=0)
            context = {'d': data,'total_employees_per_day':str(total_employees_per_day.to_json())}
            
            return render(request, template, context)

        else:
            messages.error(request, 'Please choose file to run model.')
            # handle manual employee form submission
            #form = EmployeeForm(request.POST)
            #if form.is_valid():
            #    employee = form.save(commit=False)
            #    employee.user = request.user
            #    employee.save()
            #    return redirect("organization")

    return render(request, template)
    #print(df_r.to_json())

def companyDetails(request):
    return  render(request, 'companyDetails.html')
def expenseDetails(request):
    return  render(request, 'expenseDetails.html')

def organization(request):
    departments = Department.objects.all()
    teams = Team.objects.all()
    teamFormForComboDesc = TeamFormAdd()
    choices = teamFormForComboDesc.fields['departmentID'].choices
    choice_list = [(obj.id, str(obj.departmentID)+ " - " + obj.departmentName) for obj in departments]

    # Add the choice list to the form field choices
    teamFormForComboDesc.fields['departmentID'].choices = choice_list


    if request.method == "POST":
        id = request.POST.get('id')
        if 'edit_dept' in request.POST:
            dept = Department.objects.get(id=id)
            departmentForm = DepartmentForm(request.POST, instance=dept)
            if departmentForm.is_valid():
                departmentForm.save()
        elif 'delete_dept' in request.POST:
            Department.objects.filter(id=id).delete()
        return redirect("organization")
    else:
        departmentForm = DepartmentForm()
        teamForm = teamFormForComboDesc



    employees = Employee.objects.all()
    if request.method == "POST":
        employee_id = request.POST.get('id')
        if 'edit_employee' in request.POST:
            employee = Employee.objects.get(id=employee_id)
            employeeForm = EmployeeForm(request.POST, instance=employee)
            if employeeForm.is_valid():
                employeeForm.save()
        elif 'delete_employee' in request.POST:
            Employee.objects.filter(id=employee_id).delete()
        return redirect("organization")
    else:
        employeeForm = EmployeeForm()

#    return render(request, 'organization.html', {"employees": employees, "form": form})
    return render(request, "organization.html",
                  {"allDept" :{"depts": departments, "deptForm": departmentForm},
                   "allTeamsDeptWise" : {"teams": teams, "teamForm" :  teamForm},
                   "allEmployee" : {"employees": employees, "form": employeeForm}
                   })


def postDepartment(request):
    # request should be ajax and method should be POST.
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        # get the form data
        form = DepartmentForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)

def postTeam(request):
    # request should be ajax and method should be POST.
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        # get the form data
        form = TeamFormAdd(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)

def run_model(file):
    file1 = "account\\templates\\out.csv"
    if(os.path.exists(file1) and os.path.isfile(file1)):
        os.remove(file1)
        print("file deleted")
    else:
        print("file not found")
    print("Running ML Model")

    # Read input from excel sheet
    input_data1 = pd.read_excel(file, sheet_name="Sheet5").fillna(0)
    input_data2 = pd.read_excel(file, sheet_name="Sheet6")


    # In[202]:


    j = 10
    k = 30
    l = 5

    # Extract input data
    team_list = list(input_data1["Team"].values)
    s = input_data1["Strength of Dept"].values
    c = int(input_data1.loc[0, "Total number of employees"])
    f = int(input_data1.loc[0,"Number of in person days"])
    u = int(input_data1.loc[0, "Sum of Priorities"])
    P = input_data1["Priority of each Team/Department"].values
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    a = input_data2.values
    s = s.reshape(-1,1)
    P = P.reshape(-1,1)

    input_data1.shape

    input_data2.shape


    input_data2

    print("Total number of employees = ", c)
    print("Number of in person days = ", f)
    print("Sum of Priorities = ", u)
                                          
    x = cp.Variable((k, l), boolean=True)

    objective = cp.Minimize(cp.sum(cp.multiply(s, x)))

    constraints = [
        cp.sum(cp.multiply(s, x), axis=0) <= 1.01 * c * f / 5,
        cp.sum(cp.multiply(s, x), axis=0) >= 0.99 * c * f / 5,
    #    cp.sum(x, axis=0)[:, None] <= 1,   
    ]
    for j_ in range(j):
        for l_ in range(l):
            constraints.append(cp.sum(x[np.where(a[j_,:] == 1)[0], l_]) >= 1)

    if u == 0:
        constraints.append(cp.sum(x, axis=1) == f)
    elif u >= 1:
        for k in range(k):
            if P[k] == 0:
                constraints.append(cp.sum(x[k, :]) <= f)
            elif P[k] == 1:
                constraints.append(cp.sum(x[k, :]) == l)

    problem = cp.Problem(objective, constraints)
    problem.solve()

    # Solve optimization problem and convert result to DataFrame
    result = x.value.astype(int)
    result = result  # add 1 to team indices
    df_result = pd.DataFrame(result, columns=days)
    #df_result = df_result.rename_axis('Team_Number')
    df_result['Team_Number'] = team_list
    df_result.set_index('Team_Number',inplace= True)
    #df_result.index = df_result.index + 1

    team_strength_per_day = df_result.mul(s.flatten(), axis=0)
    total_employees_per_day = team_strength_per_day.sum(axis=0)

    print(team_strength_per_day)
    print(total_employees_per_day)
    
    #time.sleep(3)
    df_result.to_csv(file1)
    return team_strength_per_day,s


def calendar(request):
    '''my_workouts = Workouts.objects.order_by('my_date').filter(
        my_date__year=year, my_date__month=month
    )'''

    teamForm = TeamForm()

    year, month = 2023 , 3
    employee_schedule  = {2: 'O', 4: 'O', 6: 'O', 7: 'H', 8: 'O', 9: 'O', 11: 'O', 12: 'O', 14: 'O', 15: 'O', 16: 'O', 17: 'H', 18: 'O', 19: 'O', 22: 'H', 23: 'O', 24: 'O', 25: 'H', 27: 'H', 29: 'H', 30: 'H'}
    cal = EmployeeCalendar(employee_schedule).formatmonth(year, month)
    return render(request, 'custom_calendar.html', {'calendar': mark_safe(cal),  'filters' : {'teamForm' : teamForm}})


def getTeams(request):
    department_id = request.GET.get('department')
    filter_manager = request.GET.get('filter_manager')
    teams = Team.objects.filter(departmentID_id=department_id).order_by('departmentID')
    if filter_manager:
        managers = Employee.objects.filter(department_id=department_id).order_by('Emp_Id')
        managerDict = [(b.id, str(b.Emp_Id)+ ' - '+b.first_name +' '+ b.last_name) for b in managers]
    return JsonResponse({'teams': [(b.id, str(b.teamNumber) + " - "+b.teamDescription) for b in teams],
                         'managers' : managerDict})

def getEmployees(request):
    department_id = request.GET.get('department')
    team_id = request.GET.get('team')
    employees = Employee.objects.filter(department_id=department_id, team_id=team_id).order_by('Emp_Id')
    return JsonResponse({'employees': [(b.id, str(b.Emp_Id)+ ' - '+b.first_name +' '+ b.last_name) for b in employees]})