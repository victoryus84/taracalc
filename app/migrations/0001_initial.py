# Generated by Django 4.2 on 2023-06-15 14:11

import app.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_activated', models.BooleanField(db_index=True, default=True, verbose_name='Прошел активацию?')),
                ('send_messages', models.BooleanField(default=True, verbose_name='Слать оповещение о новых комментариях?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Contragent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('name_full', models.CharField(blank=True, max_length=600)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('is_jur', models.BooleanField(default=True)),
                ('is_rez', models.BooleanField(default=True)),
                ('code_gov', models.CharField(blank=True, max_length=13, unique=True)),
                ('code_tva', models.CharField(blank=True, max_length=9, unique=True)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Контрагент',
                'verbose_name_plural': 'Контрагенты',
            },
        ),
        migrations.CreateModel(
            name='Vehicles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('name_full', models.CharField(blank=True, max_length=600)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('driver', models.CharField(max_length=50)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Автомобиль',
                'verbose_name_plural': 'Автомобили',
            },
        ),
        migrations.CreateModel(
            name='Nomenclature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('name_full', models.CharField(blank=True, max_length=600)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Номенклатура',
                'verbose_name_plural': 'Номенклатура',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=14, null=True, unique=True)),
                ('type', models.CharField(choices=[(app.models.DocumentType['Income'], 'Приход'), (app.models.DocumentType['Outcome'], 'Расход')], max_length=6)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('is_factura', models.BooleanField(default=False)),
                ('qty', models.IntegerField(default=1)),
                ('date', models.DateField(auto_now=True)),
                ('nomenclarture_type', models.CharField(choices=[(app.models.TaraType['Income'], 'Темное'), (app.models.TaraType['Outcome'], 'Светлое')], max_length=7)),
                ('contragent', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.contragent')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('nomenclarture', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.nomenclature')),
                ('transport', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.vehicles')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
    ]
