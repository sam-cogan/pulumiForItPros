"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources
from datetime import date

config = pulumi.Config()

tags = config.require_object("tags")
tags["dateCreated"] = date.today().isoformat()

rg = resources.ResourceGroup('resourceGroup',
                             resource_group_name=config.require(
                                 "resourceGroupName"),
                             location=config.require("location"),
                             tags=tags,
                             opts=pulumi.ResourceOptions(
                                 ignore_changes=["tags.dateCreated"],
                                 protect= True
                             )
                             )

stg_count = config.require_int("storage-count")

storageAccountIdList=[]

for i in range(stg_count):
    stg = storage.StorageAccount('stg'+str(i+1),
                                 account_name=config.require(
                                     "namePrefix")+"stg"+str(i+1),
                                 resource_group_name=rg.name,
                                 location=rg.location,
                                 sku=storage.SkuArgs(
        name=storage.SkuName.STANDARD_LRS
    ),
        kind=storage.Kind.STORAGE_V2,
        tags=tags,
        opts=pulumi.ResourceOptions(
        ignore_changes=["tags.dateCreated"],
        depends_on=[rg]
    )

    )
    storageAccountIdList.append(stg.id)

    if config.require_bool("createStorageContainer"):
        container = storage.BlobContainer("container"+str(i+1),
                                          account_name=stg.name,
                                          container_name="container1",
                                          resource_group_name=rg.name,
                                          public_access="NONE"
                                          )

storage_list = config.require_object("storage-list")

for accountDetails in storage_list:
    stg = storage.StorageAccount(accountDetails['name'],
                                 account_name=accountDetails['name'],
                                 resource_group_name=rg.name,
                                 location=rg.location,
                                 sku=storage.SkuArgs(
        name=accountDetails['sku']
    ),
        kind=storage.Kind.STORAGE_V2,
        tags=tags,
        opts=pulumi.ResourceOptions(
        ignore_changes=["tags.dateCreated"]
        
    )

    )
    storageAccountIdList.append(stg.id)

pulumi.export("secret", config.require_secret("secret1"))
pulumi.export("ResourceGroupName", rg.name)
pulumi.export("StorageAccounts", storageAccountIdList)

rgname = rg.name.apply(lambda rgName: printResourceName(rgName))


def printResourceName(resourceName):
    print("Resource Name: " + resourceName)
    print("Created On: " + str(date.today()))