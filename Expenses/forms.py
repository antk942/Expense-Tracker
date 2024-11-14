from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.forms.widgets import DateInput

from .models import Expense, Category, Notification


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name() or obj.username  # Display full name or username if full name is not available
    

class MultipleUserModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name() or obj.username  # Display full name or username if full name is not available
    

class ExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        currentUser = kwargs.pop('currentUser')  # Pass the current user to the form
        super(ExpenseForm, self).__init__(*args, **kwargs)
        
        # Set the initial value of whoPaid to the current user
        self.fields['whoPaid'].initial = currentUser

        # Set the initial value of the date field to today's date
        self.fields['date'].initial = timezone.now().date()

         # Set the initial value of splitWith to include all users if creating a new expense
        if not self.instance.pk:
            self.fields['splitWith'].initial = User.objects.all()
        else:
            self.fields['splitWith'].initial = self.instance.splitWith.all()


    splitWith = MultipleUserModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
        label='Who did you pay for?'
    )

    whoPaid = UserModelChoiceField(
        queryset=User.objects.all(),  # Fetch all users
        required=True,
        label="Who paid?",
        empty_label=None,
    )
    
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'currency', 'date', 'description', 'whoPaid', 'splitWith', 'isPaid']
        labels = {
            'isPaid': 'Is the expense resolved',
        }
        widgets = {
            'date': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class NotificationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        self.fields['dueDate'].initial = timezone.now().date()

    class Meta:
        model = Notification
        fields = ['message', 'amount', 'currency', 'bill', 'category', 'dueDate', 'frequency', 'isResolved']
        labels = {
            'isResolved': 'Is the notification resolved',
        }
        widgets = {
            'dueDate': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }