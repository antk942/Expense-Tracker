from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from ..forms import NotificationForm
from ..models import Notification
from ..communications import email


@login_required
def viewNotification(request):
    notifications = Notification.objects.all()
    return render(request, 'Expenses/Notification/viewNotification.html', {'notifications': notifications})


@login_required
def viewSingleNotification(request, id):
    notification = get_object_or_404(Notification, id=id)
    return render(request, 'Expenses/Notification/viewSingleNotification.html', {'notification': notification})


@login_required
def sendNotification(request, id):
    notification = get_object_or_404(Notification, id=id)
    email.sendNotificationEmail(notification)
    return redirect('viewNotification')


@login_required
def addNotification(request):
    nextUrl = request.GET.get('next', 'expenses')
    
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.user = request.user
            notification.save()
            return HttpResponseRedirect(nextUrl)
    else:
        form = NotificationForm()
    return render(request, 'Expenses/Notification/addNotification.html', {'form': form, 'next': nextUrl})


@login_required
def editNotification(request, id):
    notification = get_object_or_404(Notification, id=id)
    if request.method == 'POST':
        form = NotificationForm(request.POST, instance=notification)
        if form.is_valid():
            notification = form.save(commit=False)
            # Check if the notification is resolved and update dueDate if needed
            if notification.isResolved:
                if notification.frequency == 'Once':
                    notification.delete()
                    return redirect('viewNotification')
                else:
                    notification.dueDate = notification.calculateNextDate()
                    notification.isResolved = False
            notification.save()
            return redirect('viewNotification')
    else:
        form = NotificationForm(instance=notification)
    return render(request, 'Expenses/Notification/editNotification.html', {'form': form, 'notification': notification})


@login_required
def deleteNotification(request, id):
    notification = get_object_or_404(Notification, id=id)
    if request.method == 'POST':
        notification.delete()
        return redirect('viewNotification')
    return render(request, 'Expenses/Notification/confirmDeleteNotification.html', {'notification': notification})