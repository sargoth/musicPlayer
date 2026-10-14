class InvalidTurboFormMixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 422
        return response
