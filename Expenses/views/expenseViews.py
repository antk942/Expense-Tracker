from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import timezone

from ..forms import ExpenseForm
from ..models import Expense


@login_required
def addExpense(request):
    nextUrl = request.GET.get('next', 'expenses')
    categoryId = request.GET.get('category_id')
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, currentUser=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = form.cleaned_data['whoPaid']
            expense.save()
            form.save_m2m()
            return HttpResponseRedirect(nextUrl)
    else:
        form = ExpenseForm(currentUser=request.user,
                           initial={'category': categoryId, 'date': timezone.now().date()} if categoryId else {'date': timezone.now().date()})
    return render(request, 'Expenses/Expense/addExpense.html', {'form': form, 'next': nextUrl})


@login_required
def scanExpenseView(request):
    return render(request, 'Expenses/Expense/scanExpense.html')


@login_required
def viewExpense(request, id):
    expense = get_object_or_404(Expense, id=id)
    return render(request, 'Expenses/Expense/viewExpense.html', {'expense': expense})


@login_required
def editExpense(request, id):
    expense = get_object_or_404(Expense, id=id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense, currentUser=request.user)
        if form.is_valid():
            expense = form.save(commit=False)            
            expense.user = form.cleaned_data['whoPaid']
            expense.save()
            form.save_m2m()
            return redirect('viewExpense', id=expense.id)
    else:
        form = ExpenseForm(currentUser=request.user,
                           instance=expense)
    return render(request, 'Expenses/Expense/editExpense.html', {'form': form, 'expense': expense})


@login_required
def deleteExpense(request, id):
    expense = get_object_or_404(Expense, id=id)
    category = expense.category
    if request.method == 'POST':
        expense.delete()
        return redirect('viewCategory', category_id=category.id)
    return render(request, 'Expenses/Expense/confirmDelete.html', {'expense': expense})