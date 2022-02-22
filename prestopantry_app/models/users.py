from django.db import models
# from django.contrib.auth.models import User

# Table Users {
# ID int [primary key, increment]
# First_Name varchar(50)
# Last_Name varchar(50)
# Email_Address varchar(255)
# Community_Username varchar(50)
# Password_Hash UUID
# Begin_Date date
# End_Date date
# Current_Ind bit
# Created_Record datetime
# Modified_Record datetime
# }
class User(models.Model):
  id = models.AutoField(primary_key=True, auto_created=True)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.CharField(max_length=255)
  username = models.CharField(max_length=50)
  password_hash = models.CharField(max_length=256)
  begin_date = models.DateField()
  end_date = models.DateField()
  current_ind = models.BooleanField()
  created_record = models.DateTimeField()
  modified_record = models.DateTimeField()