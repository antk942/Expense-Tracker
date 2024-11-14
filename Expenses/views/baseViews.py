from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from datetime import timedelta

from ..models import Expense, Category
from ..communications import email


def redirectView(request):
    if request.user.is_authenticated:
        return redirect('expenses')
    else:
        return redirect('login')
    

@login_required
def index(request):
    categories = Category.objects.all()
    expensesByCategory = []

    for category in categories:
        expenses = Expense.objects.filter(category=category)
        if expenses.exists():  # Only add categories that have expenses
            expensesByCategory.append({
                'category': category,
                'expenses': list(expenses)
            })

    # Determine the maximum number of expenses in any category
    maxExpenses = max(len(item['expenses']) for item in expensesByCategory) if expensesByCategory else 0

    # Create a list of lists for easier iteration in the template
    expensesMatrix = []
    for i in range(maxExpenses):
        row = []
        for item in expensesByCategory:
            if i < len(item['expenses']):
                row.append(item['expenses'][i])
            else:
                row.append(None)
        expensesMatrix.append(row)

    return render(request, 'Expenses/index.html', {
        'expenses_by_category': expensesByCategory,
        'expenses_matrix': expensesMatrix,
        'categories': categories
    })


@login_required
def balanceView(request):
    users = User.objects.exclude(id=request.user.id)  # Exclude current user from the list
    currentUser = request.user
    
    finalUserBalance = calculateUserBalances(users, currentUser)

    return render(request, 'Expenses/balance.html', {'userBalance': finalUserBalance})


@login_required
def sendReminderEmailView(request):
    last_sent = request.session.get('last_email_sent')
    if last_sent:
        last_sent_time = timezone.datetime.fromisoformat(last_sent)
        if timezone.now() < last_sent_time + timedelta(hours=1):
            return JsonResponse({'status': 'error', 'message': 'You can only send a reminder once every hour.'})

    users = User.objects.exclude(id=request.user.id)  # Exclude current user from the list 
    currentUser = request.user
    finalUserBalance = calculateUserBalances(users, currentUser)
    request.session['last_email_sent'] = timezone.now().isoformat()

    if finalUserBalance:
        email.sendReminderEmail(finalUserBalance, currentUser)
        return JsonResponse({'status': 'success', 'message': 'Email sent successfully.'})    
    else:
        return JsonResponse({'status': 'error', 'message': 'No balances to send reminders for.'})


@login_required
def markUserExpensesAsPaid(request, user_id):
    if request.method == 'POST':
        currentUser = request.user
        otherUser = User.objects.get(id=user_id)
        
        # Initialize message list to collect all messages
        messages = []

        # If the current user owes the other user
        if Expense.objects.filter(user=otherUser, splitWith=currentUser, isPaid=False).exists():
            Expense.objects.filter(user=otherUser, splitWith=currentUser, isPaid=False).update(isPaid=True)
            messages.append(f'All expenses you owe to {otherUser.first_name} marked as paid.\n')
        
        # If the other user owes the current user
        if Expense.objects.filter(user=currentUser, splitWith=otherUser, isPaid=False).exists():
            Expense.objects.filter(user=currentUser, splitWith=otherUser, isPaid=False).update(isPaid=True)
            messages.append(f'All expenses owed by {otherUser.first_name} marked as paid.\n')
        
        # If there are shared expenses between the current user and the other user
        shared_expenses = Expense.objects.filter(splitWith=currentUser, isPaid=False).filter(splitWith=otherUser)
        if shared_expenses.exists():
            shared_expenses.update(isPaid=True)
            messages.append(f'All shared expenses with {otherUser.first_name} marked as paid.\n')
        
        # If no unpaid expenses found
        if not messages:
            messages.append('No unpaid expenses found.')
        
        return JsonResponse({'message': ' '.join(messages)})
    
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

    
def calculateUserBalances(users, currentUser):
    # Initialize the balances dictionary
    userBalance = {user: 0 for user in users}
    # Calculate balances for expenses paid by the current user
    for expense in Expense.objects.filter(user=currentUser, isPaid=False):
        split_users = expense.splitWith.all()
        if split_users.count() > 1:
            for user in split_users:
                if user != currentUser:
                    userBalance[user] += expense.amount / split_users.count()
        else:
            otherUser = split_users.first()
            if otherUser and otherUser != currentUser:  # Skip the current user
                userBalance[otherUser] += expense.amount       
    
    # Calculate balances for expenses owed to the current user
    for expense in Expense.objects.exclude(user=currentUser):
        if not expense.isPaid:
            split_users = expense.splitWith.all()
            if split_users.count() > 1:
                for user in split_users:
                    if user != currentUser:
                        userBalance[expense.user] -= expense.amount / split_users.count()
            else:
                userBalance[expense.user] -= expense.amount
    
    # Prepare the balance data for the template
    finalUserBalance = {
        user: {
            'balance': balance,
            'abs_balance': abs(balance),
            #'userId': users.id,
        }
        for user, balance in userBalance.items() if balance != 0
    }
    return finalUserBalance