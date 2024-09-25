from django import forms
class Datasetform(forms.Form):
    datasetname = forms.CharField(label="Enter Dataset Name", max_length=50)
    uploaddataset = forms.FileField()