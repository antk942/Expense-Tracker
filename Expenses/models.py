from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from datetime import timedelta
from calendar import monthrange


CURRENCY_CHOICES = [
        ('€', 'Euro €'),
        #('$', 'US Dollar $'),
        #('£', 'British Pound £'),
    ]


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(null=True, choices=CURRENCY_CHOICES, default='€', max_length=20)
    date = models.DateField()
    description = models.TextField(blank=True, null=True, max_length=100)
    whoPaid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='paidExpenses')
    isPaid = models.BooleanField(default=True)
    splitWith = models.ManyToManyField(User, related_name='splitExpenses', null=True)

    def get_who_paid_display(self):
        return self.whoPaid.get_full_name() or self.whoPaid.username 

    def get_split_with_display(self):
        users = self.splitWith.all()
        return ', '.join([user.get_full_name() for user in users])

    def get_is_paid_display(self):
        return 'Yes' if self.isPaid else 'No'
    
    def __str__(self):
        return f"{self.category.name}: {self.amount}{self.currency} at {self.date}"

class Notification(models.Model):

    FREQUENCY_CHOICES = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
        ('Once', 'Once')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    amount = models.DecimalField(null=True, max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(null=True, choices=CURRENCY_CHOICES, default='€', max_length=20)
    bill = models.CharField(null=True, blank= True, max_length=200)
    createdAt = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    dueDate = models.DateField(null=True, verbose_name="Due date")
    frequency = models.CharField(null=True, max_length=10, choices=FREQUENCY_CHOICES, default='Once')
    isResolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.message}: {self.amount}{self.currency} {self.frequency}"
    
    def get_is_resolved_display(self):
        return 'Yes' if self.isResolved else 'No'

    def calculateNextDate(self):
        """
        Calculate the next date based on the frequency.
        """
        if self.frequency == 'Daily':
            # Daily frequency: the next day
            return self.dueDate + timedelta(days=1)
        elif self.frequency == 'Weekly':
            # Weekly frequency: the same day of the week next week
            return self.dueDate + timedelta(weeks=1)
        elif self.frequency == 'Monthly':
            # Monthly frequency: the same day next month
            next_month = self.dueDate.month % 12 + 1
            year_increment = self.dueDate.month // 12
            year = self.dueDate.year + year_increment

            # Get the last day of the next month
            last_day_of_next_month = monthrange(year, next_month)[1]
            day = min(self.dueDate.day, last_day_of_next_month)

            return self.dueDate.replace(year=year, month=next_month, day=day)
        elif self.frequency == 'Yearly':
            # Yearly frequency: the same day next year
            year = self.dueDate.year + 1
            try:
                return self.dueDate.replace(year=year)
            except ValueError:
                # Handle leap years by setting to the last day of February
                return self.dueDate.replace(year=year, day=28)

        return self.dueDate