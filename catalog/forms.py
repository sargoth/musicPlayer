from django import forms
from .models import Album, Artist


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
