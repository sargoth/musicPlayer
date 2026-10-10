from django import forms

from playlists.models import Playlist


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ["title", "description", "cover_img_url", "tracks"]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 5
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_css = "w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-indigo-500"

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": form_css
            })
