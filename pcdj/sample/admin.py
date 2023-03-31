from django.contrib import admin

from .models import Patient, Sample, SharedComment

admin.site.register(Patient)
admin.site.register(Sample)
admin.site.register(SharedComment)
