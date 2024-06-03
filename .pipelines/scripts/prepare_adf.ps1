[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$ResourceGroupName,

  [Parameter(Mandatory = $true)]
  [string]$DataFactoryName,

  [Parameter(Mandatory = $true)]
  [string]$LandingAreaName,

  [Parameter(Mandatory = $true)]
  [string]$KeyVaultName,

  [Parameter(Mandatory = $true)]
  [string]$SQLServerName,

  [Parameter(Mandatory = $true)]
  [string]$SQLDatabaseName,

  [Parameter(Mandatory = $true)]
  [string]$FunctionAppName
)


$linkedSevicesRootPath = "orchestration_pipeline/linkedService"

$linkedService="LS_adls_knowledge_base.json"
$linkedServiceFilePath = Get-ChildItem -Path "$linkedSevicesRootPath/$linkedService"
$linkedServiceFullFilePath = $linkedServiceFilePath.FullName
$linkedService = Get-Content -Path $linkedServiceFullFilePath | ConvertFrom-Json
$linkedService.properties.typeProperties.url = "https://$LandingAreaName.dfs.core.windows.net/"
$linkedService | ConvertTo-Json -Depth 10 | Out-File -FilePath $linkedServiceFullFilePath

$linkedService="LS_key_vault.json"
$linkedServiceFilePath = Get-ChildItem -Path "$linkedSevicesRootPath/$linkedService"
$linkedServiceFullFilePath = $linkedServiceFilePath.FullName
$linkedService = Get-Content -Path $linkedServiceFullFilePath | ConvertFrom-Json
$linkedService.properties.typeProperties.baseUrl = "https://$KeyVaultName.vault.azure.net/"
$linkedService | ConvertTo-Json -Depth 10 | Out-File -FilePath $linkedServiceFullFilePath

$linkedService="LS_sql_store.json"
$linkedServiceFilePath = Get-ChildItem -Path "$linkedSevicesRootPath/$linkedService"
$linkedServiceFullFilePath = $linkedServiceFilePath.FullName
$linkedService = Get-Content -Path $linkedServiceFilePath | ConvertFrom-Json
$linkedService.properties.typeProperties.connectionString = "Integrated Security=False;Encrypt=True;Connection Timeout=30;Data Source=$SQLServerName.database.windows.net;Initial Catalog=$SQLDatabaseName"
$linkedService | ConvertTo-Json -Depth 10 | Out-File -FilePath $linkedServiceFullFilePath

$linkedService="LS_azure_func.json"
$linkedServiceFilePath = Get-ChildItem -Path "$linkedSevicesRootPath/$linkedService"
$linkedServiceFullFilePath = $linkedServiceFilePath.FullName
$linkedService = Get-Content -Path $linkedServiceFullFilePath | ConvertFrom-Json
$linkedService.properties.typeProperties.functionAppUrl = "https://$FunctionAppName.azurewebsites.net"
$linkedService.properties.typeProperties.functionKey.secretName.value = "$FunctionAppName-function-app-key"
$linkedService | ConvertTo-Json -Depth 10 | Out-File -FilePath $linkedServiceFullFilePath


$dataSetRootPath = "orchestration_pipeline/dataset"

$dataSet="DS_adls_landing.json"
$dataSetFilePath = Get-ChildItem -Path "$dataSetRootPath/$dataset"
$dataSetFullFilePath = $dataSetFilePath.FullName
$dataSet = Get-Content -Path $dataSetFullFilePath | ConvertFrom-Json
$dataSet | ConvertTo-Json -Depth 10 | Out-File -FilePath $dataSetFullFilePath

$dataSet="DS_sql_config.json"
$dataSetFilePath = Get-ChildItem -Path "$dataSetRootPath/$dataset"
$dataSetFullFilePath = $dataSetFilePath.FullName
$dataSet = Get-Content -Path $dataSetFullFilePath | ConvertFrom-Json
$dataSet | ConvertTo-Json -Depth 10 | Out-File -FilePath $dataSetFullFilePath

$dataSet="DS_sql_document_data.json"
$dataSetFilePath = Get-ChildItem -Path "$dataSetRootPath/$dataset"
$dataSetFullFilePath = $dataSetFilePath.FullName
$dataSet = Get-Content -Path $dataSetFullFilePath | ConvertFrom-Json
$dataSet | ConvertTo-Json -Depth 10 | Out-File -FilePath $dataSetFullFilePath



$pipelineRootPath = "orchestration_pipeline/pipeline"


$pipeline="PL_adls_to_knowledgebase.json"
$pipelineFilePath = Get-ChildItem -Path "$pipelineRootPath/$pipeline"
$pipelineFullFilePath = $pipelineFilePath.FullName
$pipeline = Get-Content -Path $pipelineFullFilePath | ConvertFrom-Json


$pipeline="PL_delete_data_sql_content.json"
$pipelineFilePath = Get-ChildItem -Path "$pipelineRootPath/$pipeline"
$pipelineFullFilePath = $pipelineFilePath.FullName
$pipeline = Get-Content -Path $pipelineFullFilePath | ConvertFrom-Json


$pipeline="PL_delete_files_adls_storage.json"
$pipelineFilePath = Get-ChildItem -Path "$pipelineRootPath/$pipeline"
$pipelineFullFilePath = $pipelineFilePath.FullName
$pipeline = Get-Content -Path $pipelineFullFilePath | ConvertFrom-Json


$pipeline="PL_rag_wf_CreateIndex.json"
$pipelineFilePath = Get-ChildItem -Path "$pipelineRootPath/$pipeline"
$pipelineFullFilePath = $pipelineFilePath.FullName
$pipeline = Get-Content -Path $pipelineFullFilePath | ConvertFrom-Json

$pipeline="PL_rag_wf_GetContent.json"
$pipelineFilePath = Get-ChildItem -Path "$pipelineRootPath/$pipeline"
$pipelineFullFilePath = $pipelineFilePath.FullName
$pipeline = Get-Content -Path $pipelineFullFilePath | ConvertFrom-Json


$pipeline="PL_rag_wf_GetEmbeddings.json"
$pipelineFilePath = Get-ChildItem -Path "$pipelineRootPath/$pipeline"
$pipelineFullFilePath = $pipelineFilePath.FullName
$pipeline = Get-Content -Path $pipelineFullFilePath | ConvertFrom-Json


$pipeline="PL_rag_wf_RedactPII.json"
$pipelineFilePath = Get-ChildItem -Path "$pipelineRootPath/$pipeline"
$pipelineFullFilePath = $pipelineFilePath.FullName
$pipeline = Get-Content -Path $pipelineFullFilePath | ConvertFrom-Json


$pipeline="PL_rag_wf.json"
$pipelineFilePath = Get-ChildItem -Path "$pipelineRootPath/$pipeline"
$pipelineFullFilePath = $pipelineFilePath.FullName
$pipeline = Get-Content -Path $pipelineFullFilePath | ConvertFrom-Json


$pipeline="PL_remove_document.json"
$pipelineFilePath = Get-ChildItem -Path "$pipelineRootPath/$pipeline"
$pipelineFullFilePath = $pipelineFilePath.FullName
$pipeline = Get-Content -Path $pipelineFullFilePath | ConvertFrom-Json


$pipeline="PL_wf_failures.json"
$pipelineFilePath = Get-ChildItem -Path "$pipelineRootPath/$pipeline"
$pipelineFullFilePath = $pipelineFilePath.FullName
$pipeline = Get-Content -Path $pipelineFullFilePath | ConvertFrom-Json























