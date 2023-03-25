from django import forms

class UploadDatasetForm(forms.Form):
  project_id = forms.IntegerField()
  name = forms.CharField(max_length=50)
  file = forms.FileField()
