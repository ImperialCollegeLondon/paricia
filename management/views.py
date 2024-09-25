from contextlib import suppress

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import ForeignKey, Model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import CustomUserCreationForm


def model_to_dict(instance: Model) -> dict:
    """Convert a model instance to a dictionary.

    For ForeignKey fields, the related model instance is converted to a string, so that
    a meaningful representation is shown in the dictionary instead of the primary key.

    Args:
        instance (Model): Model instance to convert.

    Returns:
        dict: Dictionary with the model instance data.
    """
    data = {}
    for field in instance._meta.fields:
        data[field.name] = field.value_from_object(instance)
        if isinstance(field, ForeignKey):
            with suppress(field.related_model.DoesNotExist):
                data[field.name] = str(
                    field.related_model.objects.get(pk=data[field.name])
                )
    return data


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class CustomDetailView(LoginRequiredMixin, DetailView):
    """Generic detail view.

    This view is used to show the details of a model object. The user must have the
    permission to view the object, otherwise a 403 error is returned.

    The view includes a form with the object data, and the context includes the URLs for
    the list, delete, and edit views, if required. They follow the pattern
    `app_label:model_name_action`. For example, the list URL for the `DataImport` model
    would be `importing:dataimport_list`.

    The permissions required to view the object are `app_label.view_model_name`. For
    example, the permission required to view a `DataImport` object would be
    `importing.view_dataimport`.

    Users need to be logged in to access this view.

    Attributes:
        template_name (str): Template to be used.
        use_back_url (bool): If True, a back URL is included in the context.
        use_delete_url (bool): If True, a delete URL is included in the context.
        use_edit_url (bool): If True, an edit URL is included in the context.
    """

    template_name: str = "object_detail.html"
    use_list_url: bool = False
    use_delete_url: bool = False
    use_edit_url: bool = False

    def get_object(self) -> Model:
        obj = get_object_or_404(self.model, pk=self.kwargs["pk"])
        if not self.request.user.has_perm(self.permission_required, obj):
            raise PermissionDenied
        return obj

    def get_form(self):
        class DetailForm(forms.ModelForm):
            class Meta:
                model = self.model
                fields = "__all__"

        return DetailForm(data=model_to_dict(self.object))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["title"] = self.model_description
        context["delete_url"] = self.delete_url if self.use_delete_url else None
        context["edit_url"] = self.edit_url if self.use_edit_url else None
        context["list_url"] = self.list_url if self.use_list_url else None
        return context

    @property
    def app_label(self) -> str:
        return self.model._meta.app_label

    @property
    def model_name(self) -> str:
        return self.model._meta.model_name

    @property
    def permission_required(self) -> str:
        return f"{self.app_label}.view_{self.model_name}"

    @property
    def list_url(self) -> str:
        return f"{self.app_label}:{self.model_name}_list"

    @property
    def delete_url(self) -> str:
        return f"{self.app_label}:{self.model_name}_delete"

    @property
    def edit_url(self) -> str:
        return f"{self.app_label}:{self.model_name}_edit"

    @property
    def model_description(self) -> str:
        return self.model._meta.verbose_name.title()
