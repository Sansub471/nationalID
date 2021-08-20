from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import UserRegisterForm, MyProfileForm, ApprovalForm

from accounts.models import Officer
from documents.models import Documents
from documents.views import get_nid_dict
from django.contrib.auth.models import User
import json
#from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Accounted Created! You can login now {username}')
            return redirect('account-login')

    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {
        'form': form,
        'title':'Register'
        })


@login_required
def profile(request):
    return render(request, 'accounts/profile.html',{
        'title':'Profile'
    })
    # will have to come back here after approval process is done


@login_required
def approvalRequest(request):
    if request.method == 'POST':
        form = MyProfileForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.posted_by = request.user
            form.save()
            messages.success(request, f'Submitted your request.')
            return redirect('profile-request')
    else:
        form = MyProfileForm()
    return render(request, 'accounts/profile-approval-request.html', {
        'form': form,
        'title':'Request'
        })

# Needs retification, review later.
@login_required
def approve(request):
    if request.method == 'POST':
        form = ApprovalForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            usrType = User.objects.get(username=request.user.username)
            form.instance.approved_by = Officer.objects.get(account=usrType) 
            form.save()
            messages.success(request, f'Request Approved')
            return redirect('profile-approve')    
    else:
        form = ApprovalForm()
    return render(request, 'accounts/profile-approve.html', {
        'form': form,
        'title':'Approve'
        })

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change-password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change-password.html', {
        'form': form,
        'title':'Change Password'
    })


@login_required
def qrcode(request):
    try:
        documents = Documents.objects.get(user=request.user)
        national_id = documents.national_id
        if national_id:                            
            return render(request, 'documents/qrcode.html', {
                'national_id': json.dumps(get_nid_dict(documents), indent=4),
                'title': 'QR Code',
            })
        else:
            return render(request, 'documents/national_id.html', {
                'messages': ['Your citizenship has not been approved yet. Your National ID and the QR Code will be created automatically once an officer has approved your citizenship.', ],
                'title': 'QR Code',
            } )
    except:
        return render(request, 'accounts/qrcode.html',{
            'title':'QR Code'
        })

