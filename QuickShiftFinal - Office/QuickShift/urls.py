"""QuickShift URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from account import views
from account.views import postDepartment

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.login,name="login"),

    path("employeeProfile/",views.employeeProfile,name="employeeProfile"),
    path("employeeProfile/schedule",views.schedule,name="schedule"),
    path("employeeProfile/timeslot",views.timeslot,name="timeslot"),
    path("employeeProfile/changeSchedule",views.changeSchedule,name="changeSchedule"),
    path("inProfile/employeeDetails",views.run_model,name="run_model"),

    #path("hrProfile/",views.calander,name="calander"),
    path("hrProfile/",views.calendar,name="calendar"),
    path("hrProfile/calander",views.calander,name="calander"),
    path("hrProfile/employeeDetails",views.employeeDetails,name="employeeDetails"),
    path("hrProfile/upload",views.upload,name="upload"),
    path("hrProfile/companyDetails",views.companyDetails,name="companyDetails"),
    path("hrProfile/expenseDetails",views.expenseDetails,name="expenseDetails"),
    path("hrProfile/organization",views.organization,name="organization"),
    path('hrProfile/organization/department', views.postDepartment, name = "post_department"),
    path('hrProfile/organization/team', views.postTeam, name = "post_team"),
    path('hrProfile/getTeams', views.getTeams, name = "get_teams"),
    path('hrProfile/getEmployees', views.getEmployees, name = "get_employees"),
]
