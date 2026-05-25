from django.db import models

class SkinDisease(models.Model):
    # HAM10000 Classes: nv, mel, bkl, bcc, akiec, vasc, df
    name = models.CharField(max_length=100, unique=True) 
    common_name = models.CharField(max_length=100, help_text="e.g., Melanoma")
    description = models.TextField()
    cause = models.TextField()
    medicine = models.TextField()
    cure_method = models.TextField()

    def __str__(self):
        return self.common_name