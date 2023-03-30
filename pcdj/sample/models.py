from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models

class Patient(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    NOT_SAY = 'N'

    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (NOT_SAY, 'Rather not say'),
    )

    name = models.CharField(max_length=255, verbose_name='Name')
    sex = models.CharField(
        max_length=1, blank=True, null=True, verbose_name='Sex', choices=SEX_CHOICES,
    )
    dob = models.DateField(verbose_name='Date of birth', blank=True, null=True)
    phone_number = models.CharField(max_length=15)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     return f'/{self.id}'


class Sample(models.Model):
    BIOPSY = 'biopsy'
    SURGICAL_RESECTION = 'surgical resection'
    OTHER = 'other'

    TYPE_CHOICES = (
        (BIOPSY, 'biopsy'),
        (SURGICAL_RESECTION, 'surgical resection'),
        (OTHER, 'other')
    )

    BLOOD = 'Blood'
    TISSUE = 'Tissue'
    URINE = 'Urine'
    STOOL = 'Stool'
    FLUID = 'Fluid'
    OTHER = 'Other'

    ORIGIN_CHOICES = (
        (BLOOD, 'blood'),
        (TISSUE, 'tissue'),
        (URINE, 'urine'),
        (STOOL, 'stool'),
        (FLUID, 'fluid'),
        (OTHER, 'other')
    )

    owner = models.ForeignKey('auth.User', related_name='owner',on_delete=models.CASCADE, blank=True, null=True)
    patient = models.ForeignKey(
        Patient,
        related_name='patient',
        on_delete=models.CASCADE,
    )
    date_collected = models.DateTimeField(
        verbose_name='Date of collection', blank=True, null=True)
    diagnosis_code = models.CharField(
        max_length=8, blank=True, null=True, verbose_name='Diagnosis Code')
    type = models.CharField(
        max_length=50,
        blank=True, null=True, verbose_name='Type', choices=TYPE_CHOICES,
    )
    origin = models.CharField(
        max_length=50,
        blank=True, null=True, verbose_name='Site of Origin', choices=ORIGIN_CHOICES,
    )
    symptoms = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    predicted_label = models.CharField(
        max_length=50,
        default='pending',
        blank=True, null=True, verbose_name='Predicted Label'
    )
    human_label = models.CharField(
        max_length=50,
        default='pending',
        blank=True, null=True, verbose_name='Human Label'
    )
    annotations = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-date_added',)
    
    # def get_absolute_url(self):
    #     return f'/{self.patient.id}/{self.id}'

    # def __str__(self):
    #     return f"{self.patient.get_full_name()}-{self.pathologist.get_full_name()}-{self.id}"

    def get_image(self):
        print("yooo", self.image)
        if self.image:
            return 'http://localhost:8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://localhost:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://localhost:8000' + self.thumbnail.url
            else:
                return ''
            
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
