from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from ..forms import CategoryForm
from ..models import Category, Expense

from datetime import datetime
from collections import defaultdict
from calendar import month_name
from PIL import Image
import matplotlib.pyplot as plt
import io


@login_required
def addCategory(request):
    nextUrl = request.GET.get('next', 'expenses')
    categories = Category.objects.values_list('name', flat=True)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            categoryName = form.cleaned_data['name'] 
            if categoryName not in categories:
                form.save()
                return HttpResponseRedirect(nextUrl)
            else:
                form = CategoryForm()
    else:
        form = CategoryForm()
    return render(request, 'Expenses/Category/addCategory.html', {'form': form, 'next': nextUrl})


@login_required
def viewCategory(request, category_id):
    # Get the current year
    current_year = datetime.now().year
    # Get the selected year from the request, default to current year if not provided
    selected_year = int(request.GET.get('year', current_year))

    # Fetch the category based on the provided category_id
    category = get_object_or_404(Category, id=category_id)

    # Filter expenses by category and current year, then order by date in descending order
    expenses = Expense.objects.filter(category=category, date__year=selected_year).order_by('-date')

    # Organize expenses by month
    monthly_expenses = defaultdict(list)
    for expense in expenses:
        month = expense.date.strftime('%B')  # e.g., "August" without the year
        monthly_expenses[month].append(expense)

    # Ensure all months are included
    for month in month_name[1:]:  # month_name[1:] gives ['January', 'February', ..., 'December']
        if month not in monthly_expenses:
            monthly_expenses[month] = []

    # Convert monthly_expenses to a list of tuples for easier iteration in the template
    monthly_expenses_items = sorted(monthly_expenses.items(), key=lambda x: datetime.strptime(x[0], '%B').month)

    return render(request, 'Expenses/Category/viewCategory.html', {
        'category': category,
        'monthly_expenses_items': monthly_expenses_items,
        'selected_year': selected_year,
        'current_year': current_year,
    })


@login_required
def editCategory(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    categories = Category.objects.values_list('name', flat=True)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            categoryName = form.cleaned_data['name'] 
            if categoryName not in categories:
                form.save()
                return redirect('viewCategory', category_id=category.id)
            else:
                form = CategoryForm(instance=category)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'Expenses/Category/editCategory.html', {
        'form': form,
        'category': category
    })

@login_required
def generateReportImage(request, category_id):
    # Get the selected year from the request, default to current year if not provided
    selected_year = int(request.GET.get('year', datetime.now().year))

    category = Category.objects.get(id=category_id)
    expenses = Expense.objects.filter(category=category, date__year=selected_year).order_by('date')

    # Group expenses by month
    monthly_expenses = {}
    for expense in expenses:
        month = expense.date.strftime('%B')
        if month not in monthly_expenses:
            monthly_expenses[month] = 0
        monthly_expenses[month] += expense.amount

    # Generate the plot
    months = list(monthly_expenses.keys())
    amounts = list(monthly_expenses.values())

    plt.figure(figsize=(10, 5))
    bars = plt.bar(months, amounts, color='green')
    plt.xlabel('Month')
    plt.ylabel('Total Expenses')
    plt.title(f'Expenses for {category.name} by Month ({selected_year})')
    plt.xticks(rotation=45)
    plt.tight_layout()

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Convert the plot image to a Pillow Image
    image = Image.open(buf)

    # Save the image to a BytesIO object
    image_buf = io.BytesIO()
    image.save(image_buf, format='PNG')
    image_buf.seek(0)

    # Return the image as a response with download headers
    response = HttpResponse(image_buf, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{category.name}_expenses_{selected_year}.png"'
    
    return response