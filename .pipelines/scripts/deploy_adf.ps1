[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$resourceGroupName,

  [Parameter(Mandatory = $true)]
  [string]$dataFactoryName
)

function CreateManagedPrivateEndpoint{
  param (
    $resourceGroupName,
    $dataFactoryName,
    $managedPrivateEndpointFilePath
  )
  $managedPrivateEndpoint = Get-Content -Path $managedPrivateEndpointFilePath | ConvertFrom-Json
  $managedPrivateEndpointName = $managedPrivateEndpoint.name
  Write-Verbose "Creating managed private endpoint definition for managed private endpoint $managedPrivateEndpointName from file $managedPrivateEndpointFilePath"

  # az datafactory managed-private-endpoint `
  # --resource-group $resourceGroupName `
  # --factory-name $dataFactoryName `
  # --managed-private-endpoint-name $managedPrivateEndpointName `
  # --managed-virtual-network-name $managedVirtualNetworkName `
  # --group-id $groupId
}

function UploadLinkedService {
  param(
    $resourceGroupName,
    $dataFactoryName,
    $linkedServiceFilePath
  )
  $linkedService = Get-Content -Path $linkedServiceFilePath | ConvertFrom-Json
  $linkedServiceName = $linkedService.name
  Write-Verbose "Creating linked service definition for linked service $linkedServiceName from file $linkedServiceFilePath"
  # az datafactory linked-service create `
  # --resource-group $resourceGroupName `
  # --factory-name $dataFactoryName `
  # --linked-service-name $linkedServiceName `
  # --properties @$dataSetFilePath  
}

function UploadDataSet {
  param (
    $resourceGroupName,
    $dataFactoryName,
    $dataSetFilePath
  )
  $dataSet = Get-Content -Path $dataSetFilePath | ConvertFrom-Json
  $dataSetName = $dataSet.name
  Write-Verbose "Creating dataset definition for dataset $dataSetName from file $dataSetFilePath"
  # az datafactory dataset create `
  # --resource-group $resourceGroupName `
  # --factory-name $dataFactoryName `
  # --dataset-name $dataSetName `
  # --properties @$dataSetFilePath

}

function UploadPipeline {
  param(
    $resourceGroupName,
    $dataFactoryName,
    $pipeLineFilePath
  )

  $pipeline = Get-Content -Path $pipeLineFilePath | ConvertFrom-Json
  $pipeLineName = $pipeline.name
  Write-Verbose "Creating pipeline definition for pipeline $pipeLineName from file $pipeLineFilePath"
  # az datafactory pipeline create `
  # --resource-group $resourceGroupName `
  # --factory-name $dataFactoryName `
  # --name $pipeLineName `
  # --pipeline @$pipeLineFilePath
}


function UploadTrigger {
  param(
    $resourceGroupName,
    $dataFactoryName,
    $triggerFilePath
  )

  $trigger = Get-Content -Path $triggerFilePath | ConvertFrom-Json
  $triggerName = $trigger.name
  Write-Verbose "Creating trigger definition for trigger $triggerName from file $triggerFilePath"
  # az datafactory trigger create `
  # --resource-group $resourceGroupName `
  # --factory-name $dataFactoryName `
  # --name $triggerName `
  # --properties @$triggerFilePath
  
  Write-Verbose "Starting trigger definition for trigger $triggerName from file $triggerFilePath"
  # az datafactory trigger start `
  # --resource-group $resourceGroupName `
  # --factory-name $dataFactoryName `
  # --name $triggerName `
}

$managedPrivateEndpointsRootPath = "orchestration_pipeline/managedVirtualNetwork/default/managedPrivateEndpoint"
$managedPrivateEndpoints = @(
  "AzureBlobStorageAccount.json",
  "AzureKeyVaultPrivateEndpoint.json",
  "AzureSqlDatabasePrivateEndpoint.json",
  "FunctionAppPrivateEndpoint.json"
)
foreach ( $managedPrivateEndpoint in $managedPrivateEndpoints) {
  $managedPrivateEndpointFilePath = Get-ChildItem -Path "$managedPrivateEndpointsRootPath/$managedPrivateEndpoint"
  $managedPrivateEndpointFullFilePath = $managedPrivateEndpointFilePath.FullName
  CreateManagedPrivateEndpoint `
    -resourceGroupName $resourceGroupName `
    -dataFactoryName $dataFactoryName `
    -managedPrivateEndpointFilePath $managedPrivateEndpointFullFilePath
}

$linkedSevicesRootPath = "orchestration_pipeline/linkedService"
$linkedServices = @(
  "LS_adls_knowledge_base.json",
  "LS_azure_func.json",
  "LS_key_vault.json",
  "LS_sql_store.json"
)
foreach ( $linkedService in $linkedServices) {
  $linkedServiceFilePath = Get-ChildItem -Path "$linkedSevicesRootPath/$linkedService"
  $linkedServiceFullFilePath = $linkedServiceFilePath.FullName
  UploadLinkedService `
    -resourceGroupName $resourceGroupName `
    -dataFactoryName $dataFactoryName `
    -linkedServiceFilePath $linkedServiceFullFilePath
}

$dataSetRootPath = "orchestration_pipeline/dataset"
$dataSets = @(
  "DS_adls_landing.json",
  "DS_sql_config.json",
  "DS_sql_document_data.json"
)
foreach ( $dataset in $dataSets) {
  $dataSetFilePath = Get-ChildItem -Path "$dataSetRootPath/$dataset"
  $dataSetFullFilePath = $dataSetFilePath.FullName
  UploadDataSet `
    -resourceGroupName $resourceGroupName `
    -dataFactoryName $dataFactoryName `
    -dataSetFilePath $dataSetFullFilePath
}

$pipelineRootPath = "orchestration_pipeline/pipeline"
$pipelines = @(
  "PL_adls_to_knowledgebase.json",
  "PL_delete_data_sql_content.json",
  "PL_delete_files_adls_storage.json",
  "PL_rag_wf_CreateIndex.json",
  "PL_rag_wf_GetContent.json",
  "PL_rag_wf_GetEmbeddings.json",
  "PL_rag_wf_RedactPII.json",
  "PL_rag_wf.json",
  "PL_remove_document.json",
  "PL_wf_failures.json"
)
foreach ( $pipeline in $pipelines) {
  $pipelineFilePath = Get-ChildItem -Path "$pipelineRootPath/$pipeline"
  $pipelineFullFilePath = $pipelineFilePath.FullName
  UploadPipeline `
    -resourceGroupName $resourceGroupName `
    -dataFactoryName $dataFactoryName `
    -pipeLineFilePath $pipelineFullFilePath
}

$triggerRootPath = "orchestration_pipeline/trigger"
$triggers = @(
  "TRG_ingest_uploaded_files.json"
)
foreach ( $trigger in $triggers) {
  $triggerFilePath = Get-ChildItem -Path "$triggerRootPath/$trigger"
  $triggerFullFilePath = $triggerFilePath.FullName
  UploadTrigger `
    -resourceGroupName $resourceGroupName `
    -dataFactoryName $dataFactoryName `
    -triggerFilePath $triggerFullFilePath
}