# Generated by Django 4.1.7 on 2023-03-01 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0005_sample_human_label_sample_predicted_label_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='origin',
            field=models.CharField(blank=True, choices=[('Blood', 'blood'), ('Tissue', 'tissue'), ('Urine', 'urine'), ('Stool', 'stool'), ('Fluid', 'fluid'), ('Other', 'other')], max_length=50, null=True, verbose_name='Site of Origin'),
        ),
    ]