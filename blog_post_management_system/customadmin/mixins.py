from django.contrib.auth import get_permission_codename


class HasPermissionsMixin(object):
    """CBV mixin which adds has_permission options to the context."""

    def has_add_permission(self, request):
        """
        Return True if the given request has permission to add an object.
        Can be overridden by the user in subclasses.
        """

        opts = self.model._meta
        codename = get_permission_codename("add", opts)

        return (
            request.user.has_perm("%s.%s" % (opts.app_label, codename))
            or request.user.is_staff
        )

    def has_change_permission(self, request, obj=None):
        """
        Return True if the given request has permission to change the given
        Django model instance, the default implementation doesn't examine the
        `obj` parameter.

        Can be overridden by the user in subclasses. In such case it should
        return True if the given request has permission to change the `obj`
        model instance. If `obj` is None, this should return True if the given
        request has permission to change *any* object of the given type.
        """

        opts = self.model._meta
        codename = get_permission_codename("change", opts)
        return (
            request.user.has_perm("%s.%s" % (opts.app_label, codename))
            or request.user.is_staff
        )

    def has_delete_permission(self, request, obj=None):
        """
        Return True if the given request has permission to change the given
        Django model instance, the default implementation doesn't examine the
        `obj` parameter.

        Can be overridden by the user in subclasses. In such case it should
        return True if the given request has permission to delete the `obj`
        model instance. If `obj` is None, this should return True if the given
        request has permission to delete *any* object of the given type.
        """

        opts = self.model._meta
        codename = get_permission_codename("delete", opts)
        return (
            request.user.has_perm("%s.%s" % (opts.app_label, codename))
            or request.user.is_staff
        )

    def has_view_permission(self, request, obj=None):
        """
        Return True if the given request has permission to view the given
        Django model instance. The default implementation doesn't examine the
        `obj` parameter.

        If overridden by the user in subclasses, it should return True if the
        given request has permission to view the `obj` model instance. If `obj`
        is None, it should return True if the request has permission to view
        any object of the given type.
        """

        opts = self.model._meta
        codename_view = get_permission_codename("view", opts)
        codename_change = get_permission_codename("change", opts)
        return (
            request.user.has_perm("%s.%s" % (opts.app_label, codename_view))
            or request.user.has_perm("%s.%s" % (opts.app_label, codename_change))
            or request.user.is_staff
        )

    def has_view_or_change_permission(self, request, obj=None):

        return (
            self.has_view_permission(request, obj)
            or self.has_change_permission(request, obj)
            or request.user.is_staff
        )

    def has_module_permission(self, request):
        """
        Return True if the given request has any permission in the given
        app label.

        Can be overridden by the user in subclasses. In such case it should
        return True if the given request has permission to view the module on
        the admin index page and access the module's index page. Overriding it
        does not restrict access to the add, change or delete views. Use
        `ModelAdmin.has_(add|change|delete)_permission` for that.
        """

        opts = self.model._meta
        return request.user.has_module_perms(opts.app_label) or request.user.is_staff


class ModelOptsMixin(object):

    """
    Mixins that add the models options to the context object
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["opts"] = self.model._meta
        return context
