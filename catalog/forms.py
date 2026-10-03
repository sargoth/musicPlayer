from django import forms
from .models import Album


class CreateAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cover_image_url"].initial = ""

        form_css = "w-full rounded-lg bg-slate-800 border-slate-700 text-white placeholder-slate-500 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm transition"

        for field in self.fields.values():
            field.widget.attrs.update({"class": form_css})
