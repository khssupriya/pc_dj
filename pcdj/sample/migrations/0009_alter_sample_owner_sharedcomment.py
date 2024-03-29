# Generated by Django 4.1.7 on 2023-03-31 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sample', '0008_sample_annotations_alter_sample_human_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='SharedComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('complete', 'complete'), ('incomplete', 'incomplete')], max_length=50, null=True, verbose_name='Status')),
                ('senderComment', models.TextField(blank=True, null=True)),
                ('receiverComment', models.TextField(blank=True, null=True)),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sharedCommentReceiver', to=settings.AUTH_USER_MODEL)),
                ('sample', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sharedComment', to='sample.sample')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sharedCommentSender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
