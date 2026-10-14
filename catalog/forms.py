import datetime

from django import forms
from .models import Album, Artist, Genre


class CreateAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cover_image_url"].initial = ""

        form_css = "w-full px-4 py-2 border border-slate-700 rounded-lg bg-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 shadow-sm transition"

        for field in self.fields.values():
            field.widget.attrs.update({"class": form_css})

    def clean_release_year(self):
        year = self.cleaned_data.get("release_year")
        current_year = datetime.date.today().year

        if year and (year < 1860 or year > current_year):
            raise forms.ValidationError(
                f"Please enter a valid year between 1860 and {current_year}"
            )

        return year


class CreateArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = "__all__"
        widgets = {
            'bio': forms.Textarea(attrs={
                "rows": 5
            }),
            "genres": forms.CheckboxSelectMultiple()
        }
        error_messages = {
            "genres": {
                "required": "You must select at least 1 genre."
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image_url"].initial = ""

        form_css = "w-full px-4 py-2 border border-slate-700 rounded-lg bg-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 shadow-sm transition"

        for field_name, field in self.fields.items():
            if field_name != "genres":
                field.widget.attrs.update({"class": form_css})
            else:
                field.widget.attrs.update({
                    "class": "rounded bg-slate-900 border-slate-700 text-white focus:ring-indigo-500"
                })


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name"]
        widgets = {
            "name": forms.Select(attrs={
                "class": "w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition"
            })
        }
