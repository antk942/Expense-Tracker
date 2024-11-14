from django.urls import path

from .views import baseViews, expenseViews, categoryViews, notificationViews, apiViews


urlpatterns = [

    # baseViews
    path('', baseViews.redirectView, name='redirectView'),
    path('expenses/', baseViews.index, name='expenses'),
    path('balance/', baseViews.balanceView, name='balance'),
    path('sendReminderEmail/', baseViews.sendReminderEmailView, name='sendReminderEmail'),
    path('markExpensesPaid/<int:user_id>/', baseViews.markUserExpensesAsPaid, name='markUserExpensesAsPaid'),    

    # expenseViews
    path('addExpense/', expenseViews.addExpense, name='addExpense'),
    path('viewExpense/<int:id>/', expenseViews.viewExpense, name='viewExpense'),
    path('editExpense/<int:id>/', expenseViews.editExpense, name='editExpense'),
    path('deleteExpense/<int:id>/', expenseViews.deleteExpense, name='deleteExpense'),

    # categoryViews
    path('addCategory/', categoryViews.addCategory, name='addCategory'),
    path('viewCategory/<int:category_id>/', categoryViews.viewCategory, name='viewCategory'),
    path('editCategory/<int:category_id>/', categoryViews.editCategory, name='editCategory'),
    path('generateReportImage/<int:category_id>/', categoryViews.generateReportImage, name='generateReportImage'),

    # notificationViews
    path('notifications/', notificationViews.viewNotification, name='viewNotification'),
    path('notification/<int:id>/', notificationViews.viewSingleNotification, name='viewSingleNotification'),
    path('sendNotification/<int:id>/', notificationViews.sendNotification, name='sendNotification'),
    path('addNotification/', notificationViews.addNotification, name='addNotification'),
    path('notification/edit/<int:id>/', notificationViews.editNotification, name='editNotification'),
    path('notification/delete/<int:id>/', notificationViews.deleteNotification, name='deleteNotification'),

    # apiViews
    path('api/yearly-expenses/<int:year>/', apiViews.getYearlyExpensesView, name='yearly-expenses'),
    path('api/monthly-expenses/<int:year>/<int:month>/', apiViews.getMonthlyExpensesView, name='monthly-expenses'),
    path('import/', apiViews.importFromExcel, name='import'),
    path('export/', apiViews.exportToExcel, name='export'),
]
