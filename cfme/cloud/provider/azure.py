from wrapanapi.azure import AzureSystem

from . import CloudProvider
from cfme.common.provider import DefaultEndpoint, DefaultEndpointForm
from utils.version import pick


class AzureEndpoint(DefaultEndpoint):
    @property
    def view_value_mapping(self):
        return {}


class AzureEndpointForm(DefaultEndpointForm):
    pass


class AzureProvider(CloudProvider):
    type_name = "azure"
    mgmt_class = AzureSystem
    db_types = ["Azure::CloudManager"]
    endpoints_form = AzureEndpointForm

    def __init__(self, name=None, endpoints=None, zone=None, key=None, region=None,
                 tenant_id=None, subscription_id=None, appliance=None):
        super(AzureProvider, self).__init__(name=name, endpoints=endpoints,
                                            zone=zone, key=key, appliance=appliance)
        self.region = region  # Region can be a string or a dict for version pick
        self.tenant_id = tenant_id
        self.subscription_id = subscription_id

    @property
    def view_value_mapping(self):
        region = pick(self.region) if isinstance(self.region, dict) else self.region
        return {
            'name': self.name,
            'prov_type': 'Azure',
            'region': region,
            'tenant_id': self.tenant_id,
            'subscription': self.subscription_id
        }

    def deployment_helper(self, deploy_args):
        """ Used in utils.virtual_machines """
        return self.data['provisioning']

    @classmethod
    def from_config(cls, prov_config, prov_key, appliance=None):
        endpoint = AzureEndpoint(**prov_config['endpoints']['default'])
        # HACK: stray domain entry in credentials, so ensure it is not there
        endpoint.credentials.domain = None
        return cls(
            name=prov_config['name'],
            region=prov_config.get('region'),
            tenant_id=prov_config['tenant_id'],
            subscription_id=prov_config['subscription_id'],
            endpoints={endpoint.name: endpoint},
            key=prov_key,
            appliance=appliance)
