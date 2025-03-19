# Azure Service Principal Setup Guide

1. Ensure you're logged in to Azure CLI with admin privileges:
```bash
az login
```

2. Get your tenant ID and store it (if you don't have it):
```bash
export tenantid=$(az account show --query tenantId -o tsv | tr '[:upper:]' '[:lower:]')
```

3. Create a new service principal with Contributor role:
```bash
# Replace SUBSCRIPTION_ID with your actual subscription ID
az ad sp create-for-rbac \
    --name "your-app-name" \
    --role Contributor \
    --scopes /subscriptions/SUBSCRIPTION_ID
```

4. From the output of the previous command, securely store the credentials:
```bash
export clientid="<appId from output>"
export clientsecret="<password from output>"
```

5. Wait for a few seconds to allow the service principal creation to propagate:
```bash
sleep 15
```

6. Test the authentication:
```bash
az login --service-principal \
    -u $clientid \
    -p $clientsecret \
    --tenant $tenantid
```

## Troubleshooting steps if authentication fails:

1. Verify the service principal is enabled:
```bash
az ad sp show --id $clientid --query "accountEnabled"
```

2. Check if the service principal has the correct role assignment:
```bash
az role assignment list --assignee $clientid
```

3. If you get "No subscriptions found" error, try adding --allow-no-subscriptions flag:
```bash
az login --service-principal \
    -u $clientid \
    -p $clientsecret \
    --tenant $tenantid \
    --allow-no-subscriptions
```

## Important Security Notes:
- Never commit or share the client secret
- Store credentials in a secure secret management system in production
- Regularly rotate the client secret
- Use the minimum required permissions (role) for your service principal
- Consider using managed identities when possible instead of service principals

After successful authentication, you can verify the connection by running:
```bash
az account show
```

This should show your subscription details and confirm you're connected with the service principal.
