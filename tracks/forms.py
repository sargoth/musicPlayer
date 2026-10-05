from django import forms

from tracks.models import Track


class CreateTrackForm(forms.ModelForm):
    class Meta:
        model = Track
        exclude = ["album"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["duration_in_seconds"].widget.attrs.update({
            "readonly": True
        })

        form_css = "w-full px-4 py-2 border border-slate-700 rounded-lg bg-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 shadow-sm transition"

        for field in self.fields.values():
            field.widget.attrs.update({"class": form_css})