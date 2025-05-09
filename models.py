from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    position = models.CharField(max_length=100)
    interview_date = models.DateField()
    feedback = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=[('Selected', 'Selected'), ('Rejected', 'Rejected'), ('On Hold', 'On Hold')],
        default='On Hold'
    )

    def __str__(self):
        return self.name

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    def __str__(self):
        return f"Leave Request by {self.employee.name}"