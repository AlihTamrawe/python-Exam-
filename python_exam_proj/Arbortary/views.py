from tkinter.tix import Tree
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages

def login(request):
    request.session['id']= 0
    user=''
    message = ""
    if request.POST:
        if request.POST.get('login')=='log':
            print(request.POST.get('login'))
            email1=request.POST.get('e1')
            pw=request.POST.get('p1')
            if User.objects.filter(email=email1):
                c = User.objects.get(email=email1)
                print(email1)
                message = ""
                request.session['email']=email1
                request.session.save()
                request.session['id']=c.id
                if bcrypt.checkpw(pw.encode(), c.password.encode()):
                    print("password match")
                    return redirect('/dashboard')
                else:
                    message = "Wrong password"
                    print('Wrong password')
    context= {
        'user':user,
        'message':message,
    }
    
    return render(request,'index1.html',context)

def register(request):
    errors={}
    if request.POST:
        if request.POST.get('register') == 'reg':
                print("Register================================================")
                if request.POST.get('pw1') == request.POST.get('pw2'):
                    errors = User.objects.validate_register(request.POST)
                    if not errors :
                        id =add_user(request.POST)
                        print(id)
                        return redirect('/')
                    else:
                        for key, value in errors.items():
                            messages.error(request, value)
                else:
                    print("confirm is Wrong")
    context ={

    }
    return render(request,'index2.html',context)

# def index(request):
#     if 'email' not in request.session :
#         print('deleted')
#         return redirect('/')
#     return
# def out(request):
#     if request.session['id']:
#         request.session.pop('id',None)
#         print('deleted')
#     return redirect('/')



def dashboard(request):

    if 'plant' in request.POST:
        return redirect('/new/tree/')
    if 'logout1' in request.POST:
        if request.session['id']:
            request.session.pop('id',None)
            print('deleted')
        return redirect('/')
    
    
    context = {
        
        'plants':Trees.objects.all(),
        'user1':User.objects.get(id=request.session['id']),
        'views':'1',
    }
    return render(request,'index.html',context)

def  account(request):
    if 'logout1' in request.POST:
        return redirect('/')
    if 'Dash' in request.POST:
        return redirect('/dashboard/')
    context = {
        'plants':Trees.objects.filter(Planted_by=User.objects.get(id=request.session['id'])),
        'user1':User.objects.get(id=request.session['id']),
        'views':'2',
    }
    return render(request,'index.html',context)

def edit_it(request,id):
    if 'logout1' in request.POST:
        return redirect('/')
    if 'Dash' in request.POST:
        return redirect('/dashboard/')
    errors={}
    if 'updated' in request.POST:
        errors = Trees.objects.validate_tree_update(request.POST)
        if not errors:
            print("begin upste")
            x=update_tree(request.POST,id)
            return redirect(f'/show/{id}/')
        else:
            print("errors")
            for key, value in errors.items():
                messages.error(request, value)
    context = {
        'tree':Trees.objects.get(id=id),
        'plants':Trees.objects.all(),
        'user1':User.objects.get(id=request.session['id']),
        'views':'3',
    }
    return render(request,'index.html',context)

def show_it(request,id):
    if 'logout1' in request.POST:
        return redirect('/')
    if 'Dash' in request.POST:
        return redirect('/dashboard/')
    print(id)
    context = {
        'tree':Trees.objects.get(id=id),
        'plants':Trees.objects.all(),
        'user1':User.objects.get(id=request.session['id']),
        'views':'4',
    }
    return render(request,'index.html',context)

def newtree(request):
    if 'logout1' in request.POST:
        return redirect('/')
    if 'Dash' in request.POST:
        return redirect('/dashboard/')
    errors={}
    if 'created' in request.POST:
        errors = Trees.objects.validate_tree_insert(request.POST)
        if not errors:
            id_tree=plant_tree(request.POST,request.session['id'])
            return redirect(f'/show/{id_tree}/')
        else:
            for key, value in errors.items():
                messages.error(request, value)
    context = {
        'user1':User.objects.get(id=request.session['id']),
        'views':'5',
    }
    return render(request,'index.html',context)

def delete_tree(request,id):
    tree = Trees.objects.get(id=id)
    tree.delete()
    return redirect('/user/account/')
def give_like(request,id):
    print('search2')
    user1=User.objects.get(id=request.session['id'])
    Trees.objects.get(id=id).visited.add(user1)
    for i in Trees.objects.get(id=id).visited.all():
        print(i)
        if i.id != request.session['id']:
            print('search')
            Trees.objects.get(id=id).visited.add(user1)
            return redirect(f'/show/{id}/')
    print('visited before')
    return redirect(f'/show/{id}/')