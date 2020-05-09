from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.web.models import Site, SiteSourceControl, SiteConfig
from azure.common.client_factory import get_client_from_cli_profile

RESOURCE_GROUP_NAME = 'sampleWebResourceGroup'
SERVICE_PLAN_NAME = 'sampleFlaskPlan'
WEB_APP_NAME = 'sampleflaskhelloworldapp123'
REPO_URL = 'https://github.com/Azure-Samples/python-docs-hello-world'

# log in
web_client = get_client_from_cli_profile(WebSiteManagementClient)

# get service plan id
service_plan = web_client.app_service_plans.get(
    RESOURCE_GROUP_NAME, SERVICE_PLAN_NAME)

# create a web app
siteConfiguration = SiteConfig(
    python_version='3.4',
)
site_async_operation = web_client.web_apps.create_or_update(
    RESOURCE_GROUP_NAME,
    WEB_APP_NAME,
    Site(
        location='eastus',
        server_farm_id=service_plan.id,
        site_config=siteConfiguration
    ),
)

site = site_async_operation.result()
print('created webapp: ' + site.default_host_name)

# continuous deployment with GitHub
source_control_async_operation = web_client.web_apps.create_or_update_source_control(
    RESOURCE_GROUP_NAME,
    WEB_APP_NAME,
    SiteSourceControl(
        is_manual_integration=True,
        is_mercurial=False,
        deployment_rollback_enabled=False,
        repo_url=REPO_URL,
        branch='master',
        # location='GitHub',
    )
)

source_control = source_control_async_operation.result()
print("added source control to: " + source_control.name + ".azurewebsites.net")
