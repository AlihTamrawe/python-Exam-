
import datetime
import re
from unicodedata import name
from django.db import models
from django.shortcuts import redirect
import bcrypt
from tkinter import CASCADE


class Usermanager(models.Manager):
    def validate_register(request,formData):
        date_format = "%Y-%m-%d"  # %Y for year, %m for month and %d for day
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(formData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if len(formData['first_name']) < 2:
            errors['first_name'] = "Title name should be at least 2 characters"
        if len(formData['last_name']) < 3:
            errors["last_name"] = "Network should be at least 3 characters"
        if len(formData['pw1']) < 8:
            errors["pw1"] = "password should be at least 8 number"
        interval=datetime.datetime.today() - datetime.datetime.strptime(formData['birthday'],date_format)
        print(interval)
        if interval/356 >= datetime.timedelta(days=13*356):
            errors['birthday'] = "the age must be more than 13 years"
        
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=45)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    birthday =models.DateTimeField()
    objects = Usermanager()

def add_user(postdata):
    first_name = postdata.get('first_name')
    last_name =  postdata.get('last_name')
    pw = postdata.get('pw1')
    pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()   
    print(pw_hash)
    email1 = postdata.get('email')
    birthday = postdata.get('birthday')
    User.objects.create(first_name=first_name,last_name=last_name,password=pw_hash,email=email1,birthday=birthday)
    last = User.objects.last()
    print('done')
    return last.id

class TreeManager(models.Manager):
    def validate_tree_insert(self,postData):
        errors ={}
        if len(postData['s2']) < 5:
            errors['s2'] = "spices name should be at least 5 characters"
        if len(postData['l2']) < 2:
            errors["l2"] = "location should be at least 2 characters"
        if len(postData['r2']) < 50:
            errors["r2"] = "Reason should be at least 50 number"
        return errors
    def validate_tree_update(self,postData):
        errors ={}
        if len(postData['s1']) < 5:
            errors['s1'] = "spices name should be at least 5 characters"
        if len(postData['l1']) < 2:
            errors["l1"] = "location should be at least 2 characters"
        if len(postData['r1']) < 50:
            errors["r1"] = "Reason should be at least 50 number"
        return errors

def plant_tree(postData,id):
    Species = postData.get('s2')
    Location = postData.get('l2')
    Reason = postData.get('r2')
    date = postData.get('d2')
    Trees.objects.create(Species=Species,Location=Location,Reason=Reason,planted_date=date,Planted_by=User.objects.get(id=id))
    print('planted succfully')
    return Trees.objects.last().id

def update_tree(postData,id_tree):
    print('kkkkk')
    tree = Trees.objects.get(id=id_tree)
    tree.Species = postData.get('s1')
    tree.Location = postData.get('l1')
    tree.Reason = postData.get('r1')
    tree.planted_date = postData.get('d1')
    tree.save()

    print('edit succfully')
    return id

class Trees(models.Model):
    Species = models.CharField(max_length=255)
    Location = models.CharField(max_length=255)
    Reason = models.CharField(max_length=255)
    planted_date = models.DateField(auto_now=True)
    Planted_by = models.ForeignKey(User,related_name="planter",on_delete=CASCADE)
    visited = models.ManyToManyField(User,related_name="visitor")
    objects = TreeManager()