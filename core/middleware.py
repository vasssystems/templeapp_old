# webapp/core/middleware.py
from django_tenants.middleware.main import TenantMainMiddleware


class TenantMiddleware(TenantMainMiddleware):
    """
        Field status can be used to temporarily disable tenant and
        block access to their site. Modifying get_tenant method from
        TenantMiddleware allows us to check if tenant should be available
        """
    def get_tenant(self, domain_model, hostname):
        tenant = super().get_tenant(domain_model, hostname)
        self.check_tenant_active(tenant)
        return tenant

    def check_tenant_active(self, tenant):
        if not tenant.status:
            raise self.TENANT_NOT_FOUND_EXCEPTION("Tenant is inactive")
            # Alternatively, return an HTTP response:
            # return HttpResponseNotFound("This tenant is currently inactive")
