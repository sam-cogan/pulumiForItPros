"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources
from datetime import date

config = pulumi.Config()

tags = config.require_object("tags")
tags["dateCreated"] = date.today().isoformat()

rg = resources.ResourceGroup('resourceGroup',
 resource_group_name= config.require("resourceGroupName"),
 location= config.require("location"),
 tags = tags
) 

stg = storage.StorageAccount('stg',
    account_name= config.require("namePrefix")+"stg01",
    resource_group_name= rg.name,
    location= rg.location,
    sku= storage.SkuArgs(
        name= storage.SkuName.STANDARD_LRS
        ),
    kind= storage.Kind.STORAGE_V2,
    tags= tags

)

if config.require_bool("createStorageContainer"):
    container = storage.BlobContainer("container",
    account_name= stg.name,
    container_name= "container1",
    resource_group_name= rg.name,
    public_access= "NONE"
    )