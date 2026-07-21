// Intentionally insecure Bicep for scanner testing only.
param location string = resourceGroup().location
param adminPassword string = 'AzureAdminPassword123!'

resource storage 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: 'polyglotlab${uniqueString(resourceGroup().id)}'
  location: location
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
  properties: {
    allowBlobPublicAccess: true
    supportsHttpsTrafficOnly: false
    minimumTlsVersion: 'TLS1_0'
    publicNetworkAccess: 'Enabled'
  }
}

resource publicContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2022-09-01' = {
  name: '${storage.name}/default/public-data'
  properties: {
    publicAccess: 'Blob'
  }
}

resource nsg 'Microsoft.Network/networkSecurityGroups@2022-09-01' = {
  name: 'polyglot-lab-open-nsg'
  location: location
  properties: {
    securityRules: [
      {
        name: 'AllowEverything'
        properties: {
          priority: 100
          access: 'Allow'
          direction: 'Inbound'
          protocol: '*'
          sourcePortRange: '*'
          destinationPortRange: '*'
          sourceAddressPrefix: '*'
          destinationAddressPrefix: '*'
        }
      }
    ]
  }
}

output leakedAdminPassword string = adminPassword
