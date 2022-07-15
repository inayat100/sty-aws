import re
from django.shortcuts import render,HttpResponse,redirect
from .models import POST,user_contact,user_reply,user_comment
from .forms import post_form,singup_form,singin_form,contact_form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.

def home(request):
    all_post = POST.objects.all().order_by('-id')
    return render(request,'index.html',{'all_post':all_post})

def contact(request):
    fm = contact_form
    if request.method == "POST":
        name = request.POST['your_name']
        email = request.POST['your_email']
        phone = request.POST['your_Number']
        write = request.POST['write']
        cont = user_contact(your_name=name,your_email=email,your_Number=phone,write=write)
        cont.save()
        messages.success(request,"Thanks fir visit our blog we will response very soon.....")
        return redirect('home')
    return render(request,'contact.html',{'form':fm})

def dasebord(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            f = post_form(request.POST,request.FILES)
            if f.is_valid():
                img = f.cleaned_data['img']
                title = f.cleaned_data['title']
                post = f.cleaned_data['post']
                u = POST(user=request.user,img=img,title=title,post=post)
                u.save()
                messages.success(request,"Post successfully created... ")
                return redirect('profile')
            else:
                messages.error(request,"somethin wrong inputs.... try again..")
                return redirect('dasebord')
        fm = post_form
        return render(request,'dase.html',{'form':fm})
    else:
        messages.error(request,"you Must be a authenticated user please login...")
        return redirect('singin')

def profile(request):
    if request.user.is_authenticated:
        all_post = POST.objects.filter(user=request.user).order_by('-id')
        return render(request,'profile.html',{'all':all_post})
    else:
        messages.error(request,"you Must be a authenticated user please login...")
        return redirect('singin')

def update(request,id):
    if request.user.is_authenticated:
        pt = POST.objects.get(pk=id)
        fm = post_form(instance=pt)
        if request.method == "POST":
            form = post_form(request.POST,request.FILES, instance=pt)
            if form.is_valid():
                form.save()
                messages.success(request,"Post successfully updated... ")
                return redirect('profile')
            else:
                messages.error(request,"somethin wrong inputs.... try again..")
                return redirect('profile')
        return render(request,'update.html',{'form':fm})
    else:
        messages.error(request,"you Must be a authenticated user please login...")
        return redirect('singin')

def delete(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pt = POST.objects.get(pk=id)
            pt.delete()
            messages.success(request,"Post successfully Deleted... ")
            return redirect('profile')
        return redirect('profile')
    else:
        messages.error(request,"you Must be a authenticated user please login...")
        return redirect('singin')

def singin(request):
    fm = singin_form
    if request.method == "POST":
        user = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=user, password=password)
        if user:
            login(request,user)
            messages.success(request,"User successfully Loged in... ")
            return redirect('profile')
        else:
            messages.error(request,"user name or password is wrong something....")
            return redirect('singin')
    return render(request,'singin.html',{'form':fm})

def singup(request):
    fm = singup_form
    if request.method == "POST":
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.error(request,"password must be same both side..")
            return redirect('singup')
        if User.objects.filter(username=username).exists():
            messages.error(request,"This user name alredy taken..")
            return redirect('singup')
        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request,"User create successfully ... ")
        return redirect('singin')
    else:
        return render(request, 'singup.html',{'form':fm})

def user_logout(request):
    logout(request)
    messages.success(request,"User successfully Logout... ")
    return redirect('/')

def full_post(request,id):
    pt = POST.objects.get(pk=id)
    tl = pt.total_like()
    # tu = pt.total_user()
    cm = user_comment.objects.filter(post=id)
    rp = user_reply.objects.all()
    all_post = POST.objects.all().order_by('?')[:4]
    if request.user.is_authenticated:
        lk = POST.objects.filter(pk=id, like=request.user.id).exists()
        return render(request, 'post.html',
                      {'post': pt, 'all_post': all_post, "total_like": tl, 'like': lk, 'comment': cm, 'reply': rp})
    else:
        return render(request, 'post.html',
                      {'post': pt, 'all_post': all_post, "total_like": tl,'comment': cm, 'reply': rp})

def like(request):
    if request.user.is_authenticated:
            if request.method == 'POST':
                p = request.POST.get('like')
                h = request.POST.get('home')
                if h:
                    dt1 = POST.objects.get(pk=h)
                    if POST.objects.filter(pk=h, like=request.user.id).exists():
                        dt1.like.remove(request.user)
                        return redirect(f'/#{h}')       
                    else:
                        dt1.like.add(request.user)
                        return redirect(f'/#{h}')
                else:
                    dt1 = POST.objects.get(pk=p)
                    if POST.objects.filter(pk=p, like=request.user.id).exists():
                        dt1.like.remove(request.user)
                        return redirect(f'/full_post/{p}/')
                    else:
                        dt1.like.add(request.user)
                        return redirect(f'/full_post/{p}/')
            else:
                messages.warning(request,"you can't do like any post by this way...")
                return redirect('/')
    else:
        messages.error(request,"you Must be a authenticated user please login...")
        return redirect('singin')

def comment(request):
    if request.user.is_authenticated:
        cmt = request.GET['comment']
        pid = request.GET['post_id']
        post = POST.objects.get(pk=pid)
        c = user_comment(user=request.user, post=post, comment=cmt)
        c.save()
        messages.success(request,"comment successfully post... ")
        return redirect(f'full_post/{pid}/')
    else:
        messages.error(request,"you Must be a authenticated user please login...")
        return redirect('singin')

def reply(request):
    if request.user.is_authenticated:
        rep = request.GET['reply']
        cm = request.GET['comment_id']
        ps = request.GET['post_id']
        post = POST.objects.get(pk=ps)
        com = user_comment.objects.get(pk=cm)
        r = user_reply(user=request.user,post=post,comment=com,reply=rep)
        r.save()
        messages.success(request,"reply successfully post... ")
        return redirect(f'full_post/{ps}/')
    else:
        messages.error(request,"you Must be a authenticated user please login...")
        return redirect('singin')

def search(request):
    searching = request.GET['search']
    se1 = POST.objects.filter(title__icontains=searching)
    se2 = POST.objects.filter(post__icontains=searching)
    allpost = se1.union(se2)
    if allpost:
        messages.success(request,"searching keys matched.....")
        return render(request, 'search.html', {'se': allpost})
    else:
        messages.error(request,"searching keys not matched.....")
        return render(request,'search.html',{'no':searching})

