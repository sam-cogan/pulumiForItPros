"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources
from datetime import date

tags = {
    "OwnedBy" : "Sam Cogan",
    "DateCreated" : date.today().isoformat()
 }

createStorageContainer=False

rg = resources.ResourceGroup('resourceGroup',
 resource_group_name= "PulumiForItPros",
 location= "WestEurope",
 tags = tags
) 

stg = storage.StorageAccount('stg',
    account_name= "itprosstg01",
    resource_group_name= rg.name,
    location= rg.location,
    sku= storage.SkuArgs(
        name= storage.SkuName.STANDARD_LRS
        ),
    kind= storage.Kind.STORAGE_V2,
    tags= tags

)

if createStorageContainer:
    container = storage.BlobContainer("container",
    account_name= stg.name,
    container_name= "container1",
    resource_group_name= rg.name,
    public_access= "NONE"
    )