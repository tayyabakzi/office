from django import forms

from .Department import Department, Team
from .EmployeeSchedule import EmployeeSchedule
from .models import Employee


class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
    ## add a "form-control" class to each form input
    ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
            'class': 'form-control',
        })

        choice_list = [('', '---------')]+[(obj.id, str(obj.departmentID)+ " - " + obj.departmentName) for obj in Department.objects.all()]
        self.fields['department'].choices = choice_list


    class Meta:
        model = Employee
        fields = ("__all__")
        exclude = ("is_on_schedule",)

    is_on_schedule = forms.BooleanField(required=False)

#    Emp_Id = forms.IntegerField(label="employee ID")
#    Name = forms.CharField(label="full name", max_length=50)
#    Scheduling = forms.CharField(label="scheduling", max_length=50)
#    Department = forms.CharField(label='department', max_length=100)
#    Team = forms.CharField(label='team', max_length=50)
#    Manager_Name = forms.CharField(label='manager name', max_length=50)
#    Manager_Id = forms.IntegerField(label='manager ID')
#    Email = forms.EmailField(label='email')
#
#    class Meta:
#        model = Employee
#        exclude = ("user",)



class DepartmentForm(forms.ModelForm):
    departmentID = forms.IntegerField(label="Department ID")
    departmentName = forms.CharField(label="Department Name", max_length=100)

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Department
        fields = ("__all__")


class EmployeeScheduleForm(forms.ModelForm):
    Emp_Id = forms.IntegerField(label="Employee ID")
    #departmentName = forms.CharField(label="DepartmentName", max_length=100)

    def __init__(self, *args, **kwargs):
        super(EmployeeScheduleForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = EmployeeSchedule
        fields = ("__all__")


class TeamForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Select an option")
    team = forms.ModelChoiceField(queryset=Team.objects.none())
    employee = forms.ModelChoiceField(queryset=Employee.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

        choice_list = [('', '---------')]+[(obj.id, str(obj.departmentID)+ " - " + obj.departmentName) for obj in Department.objects.all()]
        self.fields['department'].choices = choice_list

        #if 'department' in self.data:
        #    try:
        #        department_id = int(self.data.get('department'))
        #        self.fields['team'].queryset = Team.objects.filter(departmentID_id=department_id).order_by('teamNumber')
        #    except (ValueError, TypeError):
        #        pass
        #elif 'department' in self.data and 'team' in self.data:
        #    try:
        #        department_id = int(self.data.get('department'))
        #        self.fields['employee'].queryset = Employee.objects.filter(department_id=department_id).order_by('departmentID')
        #    except (ValueError, TypeError):
        #        pass
        #
        #elif self.instance.pk:
        #     self.fields['team'].queryset = self.instance.department.team_set.order_by('teamNumber')


class TeamFormAdd(forms.ModelForm):
    #department = forms.ModelChoiceField(queryset=Department.objects.all(), label="Department")
    #teamNumber = forms.IntegerField(label="Team #")
    #description = forms.CharField(label="Description", max_length=100)

    def __init__(self, *args, **kwargs):
        super(TeamFormAdd, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Team
        fields = ("__all__")