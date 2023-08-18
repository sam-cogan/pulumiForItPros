import pulumi
import pulumi_azure_native as azure_native

import_stg = azure_native.storage.StorageAccount("import-stg",
    access_tier=azure_native.storage.AccessTier.HOT,
    account_name="pulimport001",
    kind="StorageV2",
    allow_blob_public_access= True,
    allow_shared_key_access= True,
    enable_https_traffic_only= True,
    minimum_tls_version= "TLS1_2",
    location="westeurope",
    resource_group_name="pulumi-import",
    sku=azure_native.storage.SkuArgs(
        name="Standard_RAGRS",
    ),
    opts=pulumi.ResourceOptions(  ))