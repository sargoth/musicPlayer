from django import forms

from tracks.models import Track


class CreateTrackForm(forms.ModelForm):
    class Meta:
        model = Track
        exclude = ["album"]
        widgets = {
            "duration_in_seconds": forms.HiddenInput(),
            "audio_file": forms.FileInput(
                attrs={
                    "class": (
                        "block w-full text-xs text-slate-400 "
                        "file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 "
                        "file:text-xs file:font-semibold "
                        "file:bg-indigo-600 file:text-white "
                        "hover:file:bg-indigo-500 file:cursor-pointer transition"
                    )
                }
            )
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        form_css = "w-full px-4 py-2 border border-slate-700 rounded-lg bg-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 shadow-sm transition"

        for field_name, field in self.fields.items():
            if field_name != "audio_file":
                field.widget.attrs.update({"class": form_css})

    def clean(self):
        cleaned_data = super().clean()
        audio_file = cleaned_data.get("audio_file")
        track_url = cleaned_data.get("track_url")

        if not audio_file and not track_url:
            message = "Please provide an audio file or a direct link. Both cannot be empty."
            self.add_error("audio_file", message)
            self.add_error("track_url", message)
        elif audio_file and track_url:
            message = "Please provide a single audio source. Either a link or a file."
            self.add_error("audio_file", message)
            self.add_error("track_url", message)

        return cleaned_data
