from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView
from django.views.generic.edit import UpdateView
from django_filters import FilterSet
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from guardian.shortcuts import get_objects_for_user

from .forms import CustomUserCreationForm, UserProfileForm
from .models import User
from .permissions import get_queryset
from .tools import get_deleted_objects


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "registration/profile.html"
    success_url = reverse_lazy("user_profile")

    def get_object(self, queryset=None):
        return self.request.user


class URLMixin:
    """Mixin to add URLs to a view.

    This mixin adds the URLs for the list, create, edit, and delete views to a view. The
    URLs follow the pattern `app_label:model_name_action`. For example, the list URL for
    the `DataImport` model would be `importing:dataimport_list`.

    Attributes:
        app_label (str): Application label.
        model_name (str): Model name.
    """

    model: Model

    @property
    def app_label(self) -> str:
        return self.model._meta.app_label

    @property
    def model_name(self) -> str:
        return self.model._meta.model_name

    @property
    def list_url(self) -> str:
        return f"{self.app_label}:{self.model_name}_list"

    @property
    def create_url(self) -> str:
        return f"{self.app_label}:{self.model_name}_create"

    @property
    def edit_url(self) -> str:
        return f"{self.app_label}:{self.model_name}_edit"

    @property
    def delete_url(self) -> str:
        return f"{self.app_label}:{self.model_name}_delete"

    @property
    def detail_url(self) -> str:
        return f"{self.app_label}:{self.model_name}_detail"

    @property
    def model_description(self) -> str:
        return self.model._meta.verbose_name.title()

    @property
    def title(self) -> str:
        return self.model._meta.verbose_name_plural.title()


class CustomDetailView(URLMixin, LoginRequiredMixin, DetailView):
    """Generic detail view.

    This view is used to show the details of a model object. The user must have the
    permission to view the object, otherwise a 403 error is returned.

    The view includes a form with the object data, and the context includes the URLs for
    the list, delete, and edit views.

    The permissions required to view the object are `app_label.view_model_name`. For
    example, the permission required to view a `DataImport` object would be
    `importing.view_dataimport`.

    Users need to be logged in to access this view.

    Attributes:
        template_name (str): Template to be used.
        fields (str): Fields to be shown in the form.
    """

    template_name: str = "object_detail.html"
    fields = "__all__"

    def get_object(self) -> Model:
        obj = get_object_or_404(self.model, pk=self.kwargs["pk"])
        if not self.request.user.has_perm(self.permission_required, obj):
            raise PermissionDenied
        return obj

    def get_inline(self) -> dict | None:
        """Return the inline data for the format.

        If provided, this method should return a dictionary with the inline data to be
        shown in the detail view. The dictionary should have the following keys:

        - title: Title of the inline data.
        - header: List with the header of the table.
        - objects: List with the objects to be shown in the table. Each object should be
            a list with the same length as the header.

        Returns:
            dict | None: Inline data for the format.
        """
        return None

    def get_form(self):
        class DetailForm(forms.ModelForm):
            class Meta:
                model = self.model
                fields = self.fields

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field in self.fields.keys():
                    self.fields[field].widget.attrs["disabled"] = True
                    self.fields[field].widget.attrs["readonly"] = True

        return DetailForm(instance=self.object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["inline"] = self.get_inline()
        context["title"] = self.model_description
        context["delete_url"] = self.delete_url
        context["edit_url"] = self.edit_url
        context["list_url"] = self.list_url
        context["pk"] = self.object.pk
        return context

    @property
    def permission_required(self) -> str:
        return f"{self.app_label}.view_{self.model_name}"


class CustomTableView(URLMixin, LoginRequiredMixin, SingleTableMixin, FilterView):
    """This view is used to show a list of model objects.

    The view includes a table with the objects, and the context includes the title of
    the view, the refresh URL, and the URL to create a new object.

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

    def get_filterset_class(self):
        """Return the filter class for the view.

        If no filter class is provided in the view, the default filter for the model is
        used. The default filter is created by the `FilterSet` class, and includes only
        the 'visibility'.
        """
        if not self.filterset_class:

            class VisbilityFilter(FilterSet):
                class Meta:
                    model = self.model
                    fields = ["visibility"]

            return VisbilityFilter

        return super().get_filterset_class()

    @property
    def permission_required(self) -> str:
        return f"{self.app_label}.view_{self.model_name}"


class CustomEditView(URLMixin, LoginRequiredMixin, UpdateView):
    """Generic edit view.

    This view is used to edit a model object. The user must have the permission to edit
    the object, otherwise a 403 error is returned.

    The view includes a form with the object data, and the context includes the title of
    the view and the URL to the list view.

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
    exclude: list[str] = []

    def get_form_class(self) -> forms.BaseModelForm:
        class CustomCreateForm(forms.ModelForm):
            foreign_key_fields = self.foreign_key_fields

            class Meta:
                model = self.model
                fields = self.fields
                exclude = self.exclude

            def __init__(self, *args, **kwargs):
                """Filter the queryset for foreign key fields based on the user.

                Otherwise, the user would see all objects, even those they don't have
                access to. We need to pop the user from the kwargs, as it's not a valid
                argument for the form.
                """
                user = kwargs.pop("user") if "user" in kwargs else None
                super().__init__(*args, **kwargs)
                if user:
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
    def success_url(self) -> str:
        return reverse_lazy(self.detail_url, kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        """Add the user to the form kwargs, so we can filter the options."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class CustomCreateView(URLMixin, LoginRequiredMixin, CreateView):
    """Generic create view.

    This view is used to create a new model object. The user must have the permission to
    create the object, otherwise a 403 error is returned.

    The view includes a form with the object data, and the context includes the title of
    the view and the URL to the list view.

    If provided, the `foreign_key_fields` attribute is used to limit the queryset for
    foreign key fields.

    If successful, the view redirects to the detail view of the created object.

    Users need to be logged in to access this view.

    Attributes:
        template_name (str): Template to be used.
    """

    template_name = "object_create.html"
    foreign_key_fields: list[str] = []
    exclude: list[str] = []

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
                exclude = self.exclude

            def __init__(self, *args, **kwargs):
                """Filter the queryset for foreign key fields based on the user.

                Otherwise, the user would see all objects, even those they don't have
                access to. We need to pop the user from the kwargs, as it's not a valid
                argument for the form.
                """
                user = kwargs.pop("user") if "user" in kwargs else None
                super().__init__(*args, **kwargs)
                if user:
                    for field in self._meta.model._meta.fields:
                        if field.name in self.foreign_key_fields:
                            self.fields[field.name].queryset = get_queryset(field, user)

        return CustomCreateForm

    def form_valid(self, form: forms.ModelForm) -> HttpResponse:
        """Set the owner of the object to the current user.

        This is done before saving the object to the database.

        Args:
            form (forms.ModelForm): Form with the object data.

        Returns:
            HttpResponse: Redirect to the detail view of the created object.
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)

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


class CustomDeleteView(URLMixin, LoginRequiredMixin, DeleteView):
    """Generic delete view.

    This view is used to delete a model object. The user must have the permission to
    delete the object, otherwise a 403 error is returned. A confirmation page is shown
    with the related objects that will be deleted.

    The permissions required to delete the object are `app_label.delete_model_name`. For
    example, the permission required to delete a `DataImport` object would be
    `importing.delete_dataimport`.

    If successful, the view redirects to the list view.

    Users need to be logged in to access this view.

    Attributes:
        template_name (str): Template to be used.
    """

    template_name = "object_delete.html"

    def get_object(self) -> Model:
        obj = super().get_object()
        if not self.request.user.has_perm(
            f"{self.app_label}.delete_{self.model_name}", obj
        ):
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])

        context["deletable_objects"] = deletable_objects
        context["model_count"] = dict(model_count).items()
        context["protected"] = protected
        context["title"] = self.model_description
        context["detail_url"] = self.detail_url
        context["pk"] = self.object.pk
        return context

    @property
    def success_url(self) -> str:
        return reverse_lazy(self.list_url)
