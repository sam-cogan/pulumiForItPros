"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources
from pulumi_azure_native import provider
import pulumi_aws_native

from datetime import date

config = pulumi.Config()

tags = config.require_object("tags")
tags["dateCreated"] = date.today().isoformat()

rg = resources.ResourceGroup('rg',
                             resource_group_name=config.require(
                                 "resourceGroupName"),
                             location=config.require("location"),
                             tags=tags,
                             opts=pulumi.ResourceOptions(
                                 ignore_changes=["tags.dateCreated"],
                                 protect=True,
                                 aliases=["resourceGroup"],
                                 delete_before_replace=True,

                             )
                             )

stg_count = config.require_int("storage-count")

storageAccountIdList = []

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
        depends_on=[rg],
        parent= [rg]
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


secondSubProvider = provider.Provider("secondSubProvider",
    subscription_id= "484f613c-dd2a-45b3-a8ea-6f87592ddb18",
)


secondSubStorage = storage.StorageAccount(
    "secondSubStorage1",
    account_name="stgsub2001",
    resource_group_name="crossSubscriptionDeployment",
    location=rg.location,
    sku=storage.SkuArgs(
    name="Standard_LRS"
),
    kind=storage.Kind.STORAGE_V2,
    tags=tags,
    opts=pulumi.ResourceOptions(
    ignore_changes=["tags.dateCreated"],
    provider= secondSubProvider

) 
)

awsProvider = pulumi_aws_native.provider.Provider("awsProvider",
    access_key= "zadsadsa",
    secret_key= "zsadasdasd"
)


pulumi.export("secret", config.require_secret("secret1"))
pulumi.export("ResourceGroupName", rg.name)
pulumi.export("StorageAccounts", storageAccountIdList)

rgname = rg.name.apply(lambda rgName: printResourceName(rgName))


def printResourceName(resourceName):
    print("Resource Name: " + resourceName)
    print("Created On: " + str(date.today()))
