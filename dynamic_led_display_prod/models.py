# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CustomuserCustomuser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    email = models.CharField(unique=True, max_length=254)
    is_editor = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'CustomUser_customuser'


class CustomuserCustomuserGroups(models.Model):
    customuser = models.ForeignKey(CustomuserCustomuser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'CustomUser_customuser_groups'
        unique_together = (('customuser', 'group'),)


class CustomuserCustomuserUserPermissions(models.Model):
    customuser = models.ForeignKey(CustomuserCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'CustomUser_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

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
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class ControllerElements(models.Model):
    element_name = models.CharField(max_length=255)
    code = models.TextField()

    class Meta:
        managed = False
        db_table = 'controller_elements'


class ControllerPanel(models.Model):
    styles = models.TextField(blank=True, null=True)
    sequence = models.JSONField(blank=True, null=True)
    channel_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'controller_panel'


class ControllerPanelPrograms(models.Model):
    panel = models.ForeignKey(ControllerPanel, models.DO_NOTHING)
    programs = models.ForeignKey('ControllerPrograms', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'controller_panel_programs'
        unique_together = (('panel', 'programs'),)


class ControllerPrograms(models.Model):
    program_name = models.CharField(unique=True, max_length=255)
    code = models.TextField(blank=True, null=True)
    running_time = models.PositiveIntegerField()
    panel_code = models.TextField(blank=True, null=True)
    animation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'controller_programs'


class ControllerProgramsElements(models.Model):
    programs = models.ForeignKey(ControllerPrograms, models.DO_NOTHING)
    elements = models.ForeignKey(ControllerElements, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'controller_programs_elements'
        unique_together = (('programs', 'elements'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(CustomuserCustomuser, models.DO_NOTHING)
    action_time = models.DateTimeField()

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


class SerialCommRs232(models.Model):
    rtc = models.CharField(db_column='RTC', max_length=255)  # Field name made lowercase.
    avgespeed = models.CharField(db_column='AvgeSpeed', max_length=255)  # Field name made lowercase.
    avgetemp = models.CharField(db_column='AvgeTemp', max_length=255)  # Field name made lowercase.
    avgehum = models.CharField(db_column='AvgeHum', max_length=255)  # Field name made lowercase.
    avgesr = models.CharField(db_column='AvgeSr', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'serial_comm_rs232'


class SerialCommRs485(models.Model):
    rtc = models.CharField(db_column='RTC', max_length=255)  # Field name made lowercase.
    avgespeed = models.CharField(db_column='AvgeSpeed', max_length=255)  # Field name made lowercase.
    avgetemp = models.CharField(db_column='AvgeTemp', max_length=255)  # Field name made lowercase.
    avgehum = models.CharField(db_column='AvgeHum', max_length=255)  # Field name made lowercase.
    avgesr = models.CharField(db_column='AvgeSr', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'serial_comm_rs485'
