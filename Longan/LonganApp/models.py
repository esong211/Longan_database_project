# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class CareerFair(models.Model):
    cf_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    year = models.DateField()
    semester = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'CareerFair'


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    address = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=8, decimal_places=4)
    longitude = models.DecimalField(max_digits=8, decimal_places=4)

    class Meta:
        managed = True
        db_table = 'Company'

    @classmethod
    def create(cls, company_id, name, address, website, latitude, longitude):
        company = cls(company_id=company_id, name=name, address=address, website=website, latitude=latitude, longitude=longitude)
        # do something with the book
        return company


class Industry(models.Model):
    industry_id = models.AutoField(primary_key=True)
    color = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'Industry'


class Major(models.Model):
    major_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'Major'


class School(models.Model):
    school_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'School'


class User(models.Model):
    email = models.CharField(primary_key=True, max_length=255)
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    gradyear = models.IntegerField(db_column='gradYear')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User'


class Attends(models.Model):
    companyid = models.IntegerField(db_column='companyID', blank=True, null=True)  # Field name made lowercase.
    cfid = models.IntegerField(db_column='cfID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'attends'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cinindustry(models.Model):
    company_id = models.IntegerField()
    industry_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cinIndustry'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Favorites(models.Model):
    company_name = models.CharField(max_length=255)
    email = models.CharField(max_length=254)

    class Meta:
        managed = True
        db_table = 'favorites'
        unique_together = (('company_name', 'email'),)


class Hostedby(models.Model):
    cfid = models.IntegerField(db_column='cfID', primary_key=True)  # Field name made lowercase.
    schoolid = models.IntegerField(db_column='schoolID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hostedBy'


class Prefers(models.Model):
    email = models.CharField(max_length=254)
    industry_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'prefers'
        unique_together = (('industry_name', 'email'),)


class Recruitedby(models.Model):
    schoolid = models.IntegerField(db_column='schoolID', blank=True, null=True)  # Field name made lowercase.
    companyid = models.IntegerField(db_column='companyID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'recruitedBy'
