from django.db import models
from user.models import User
from .managers import *

# Create your models here.
class ReportCase(models.Model):
	report_case_id = models.AutoField(primary_key=True)
	objects = ReportCaseManager()
	datetime_created = models.DateTimeField(
		auto_now=True
	)
	pass

class ReportState(models.Model):
	report_state_id = models.AutoField(primary_key=True)
	objects = ReportStateManager()
	pass

class ImageProof(models.Model):
	image_proof_id = models.AutoField(primary_key=True)
	objects = ImageProofManager()
	pass

class VideoProof(models.Model):
	video_id = models.AutoField(primary_key=True)
	objects = VideoProofManager()
	pass

