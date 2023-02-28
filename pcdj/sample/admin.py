from django.contrib import admin

from .models import Patient, Sample

admin.site.register(Patient)
admin.site.register(Sample)
