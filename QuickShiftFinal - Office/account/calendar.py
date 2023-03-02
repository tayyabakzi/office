from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc


class EmployeeCalendar(HTMLCalendar):

    def __init__(self, workouts):
        super(EmployeeCalendar, self).__init__()
        #self.workouts = self.group_by_day(workouts)
        self.workouts = workouts
        cssclasses = [style + " text-nowrap" for style in
                      HTMLCalendar.cssclasses]
    cssclass_month_head = "text-center month-head"
    cssclass_month = "text-center month table"
    cssclass_year = "text-italic lead"

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.workouts:
                #cssclass += ' success'
                body = ['<ul>']
                for workout in self.workouts[day]:
                    if workout == 'O':
                        cssclass += ' success'
                        body.append(esc('Onsite'))
                    else:
                        cssclass += ' wfh'
                        body.append(esc('Remote'))
                    #body.append('<li>')
                    #body.append('<a href="%s">' % workout.get_absolute_url())

                    #body.append('</a></li>')
                    #body.append('</li>')
                #body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        cssclass = self.cssclasses[month]
        cssclass += ' table'
        return super(EmployeeCalendar, self).formatmonth(year, month)

    '''def group_by_day(self, workouts):
        field = lambda workout: workout.performed_at.day
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )'''

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
