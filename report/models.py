from django.db import models
from user.models import User
from .managers import *

# Create your models here.
class ReportCase(models.Model):
	objects = ReportCaseManager()
	pass

class ReportState(models.Model):
	objects = ReportStateManager()
	pass

class ImageProof(models.Model):
	objects = ImageProofManager()
	pass

class VideoProof(models.Model):
	objects = VideoProofManager()
	pass

