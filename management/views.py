from contextlib import suppress

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import ForeignKey, Model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import UpdateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from guardian.shortcuts import get_objects_for_user

from .forms import CustomUserCreationForm
from .permissions import get_queryset


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
    show_delete_btn: bool = False

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
        context["delete_url"] = self.delete_url if self.show_delete_btn else None
        context["edit_url"] = self.edit_url
        context["list_url"] = self.list_url
        context["pk"] = self.object.pk
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


class CustomTableView(LoginRequiredMixin, SingleTableMixin, FilterView):
    """This view is used to show a list of model objects.

    The view includes a table with the objects, and the context includes the title of
    the view, the refresh URL, and the URL to create a new object, if required. They
    follow the pattern `app_label:model_name_action`. For example, the list URL for the
    `DataImport` model would be `importing:dataimport_list`.

    The permissions required to view the objects are `app_label.view_model_name`. For
    example, the permission required to view a `DataImport` object would be
    `importing.view_dataimport`.

    If provided, the `filter_class` attribute is used to create a filter form on top
    of the table.

    Users need to be logged in to access this view.

    Attributes:
        model (Model): Model to be used.
        table_class (tables.Table): Table class to be used.
        filterset_class (filters.FilterSet): Filter class to be used. If not provided,
            the model's default filter is used.
        template_name (str): Template to be used.
        paginate_by (int): Number of objects per page.
        show_refresh_btn (bool): If True, a refresh url is included in the context.
        show_new_btn (bool): If True, a create url is included in the context.
    """

    template_name = "table.html"
    paginate_by = 10

    def get_queryset(self):
        return get_objects_for_user(self.request.user, self.permission_required)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["list_url"] = self.list_url
        context["create_url"] = self.create_url
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
    def title(self) -> str:
        return self.model._meta.verbose_name_plural.title()

    @property
    def list_url(self) -> str:
        return f"{self.app_label}:{self.model_name}_list"

    @property
    def create_url(self) -> str:
        return f"{self.app_label}:{self.model_name}_create"


class CustomEditView(LoginRequiredMixin, UpdateView):
    """Generic edit view.

    This view is used to edit a model object. The user must have the permission to edit
    the object, otherwise a 403 error is returned.

    The view includes a form with the object data, and the context includes the title of
    the view and the URL to the list view. They follow the pattern
    `app_label:model_name_action`. For example, the list URL for the `DataImport` model
    would be `importing:dataimport_list`.

    The permissions required to edit the object are `app_label.change_model_name`. For
    example, the permission required to edit a `DataImport` object would be
    `importing.change_dataimport`.

    If successful or cancelled, the view redirects to the detail view of the created
    object.

    Users need to be logged in to access this view.

    Attributes:
        template_name (str): Template to be used.
    """

    template_name = "object_edit.html"
    foreign_key_fields: list[str] = []

    def get_form_class(self) -> forms.BaseModelForm:
        class CustomCreateForm(forms.ModelForm):
            foreign_key_fields = self.foreign_key_fields

            class Meta:
                model = self.model
                fields = self.fields

            def __init__(self, *args, **kwargs):
                user = kwargs.pop("user")
                super().__init__(*args, **kwargs)
                for field in self._meta.model._meta.fields:
                    if field.name in self.foreign_key_fields:
                        self.fields[field.name].queryset = get_queryset(field, user)

        return CustomCreateForm

    def get_object(self) -> Model:
        obj = super().get_object()
        if not self.request.user.has_perm(
            f"{self.app_label}.change_{self.model_name}", obj
        ):
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.model_description
        context["detail_url"] = self.detail_url
        context["pk"] = self.object.pk
        return context

    @property
    def app_label(self) -> str:
        return self.model._meta.app_label

    @property
    def model_name(self) -> str:
        return self.model._meta.model_name

    @property
    def model_description(self) -> str:
        return self.model._meta.verbose_name.title()

    @property
    def success_url(self) -> str:
        return reverse_lazy(self.detail_url, kwargs={"pk": self.object.pk})

    @property
    def detail_url(self) -> str:
        return f"{self.app_label}:{self.model_name}_detail"

    def get_form_kwargs(self):
        """Add the user to the form kwargs, so we can filter the options."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class CustomCreateView(LoginRequiredMixin, CreateView):
    """Generic create view.

    This view is used to create a new model object. The user must have the permission to
    create the object, otherwise a 403 error is returned.

    The view includes a form with the object data, and the context includes the title of
    the view and the URL to the list view. They follow the pattern
    `app_label:model_name_action`. For example, the list URL for the `DataImport` model
    would be `importing:dataimport_list`.

    If provided, the `foreign_key_fields` attribute is used to limit the queryset for
    foreign key fields.

    If successful, the view redirects to the detail view of the created object.

    Users need to be logged in to access this view.

    Attributes:
        template_name (str): Template to be used.
    """

    template_name = "object_create.html"
    foreign_key_fields: list[str] = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.model_description
        context["list_url"] = self.list_url
        return context

    def get_form_class(self) -> forms.BaseModelForm:
        class CustomCreateForm(forms.ModelForm):
            foreign_key_fields = self.foreign_key_fields

            class Meta:
                model = self.model
                fields = self.fields

            def __init__(self, *args, **kwargs):
                user = kwargs.pop("user") if "user" in kwargs else None
                super().__init__(*args, **kwargs)
                if user:
                    for field in self._meta.model._meta.fields:
                        if field.name in self.foreign_key_fields:
                            self.fields[field.name].queryset = get_queryset(field, user)

        return CustomCreateForm

    @property
    def app_label(self) -> str:
        return self.model._meta.app_label

    @property
    def model_name(self) -> str:
        return self.model._meta.model_name

    @property
    def model_description(self) -> str:
        return self.model._meta.verbose_name.title()

    @property
    def success_url(self) -> str:
        return reverse_lazy(self.detail_url, kwargs={"pk": self.object.pk})

    @property
    def detail_url(self) -> str:
        return f"{self.app_label}:{self.model_name}_detail"

    @property
    def list_url(self) -> str:
        return f"{self.app_label}:{self.model_name}_list"

    def get_form_kwargs(self):
        """Add the user to the form kwargs, so we can filter the options."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
