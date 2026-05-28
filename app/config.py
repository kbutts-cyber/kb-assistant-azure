from azure.identity import ManagedIdentityCredential, DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

def get_openai_key() -> str:
    key_vault_url = os.environ["KEY_VAULT_URL"]
    
    try:
        credential = ManagedIdentityCredential()
        client = SecretClient(vault_url=key_vault_url, credential=credential)
        secret = client.get_secret("azure-openai-key")
        return secret.value
    except Exception:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_url, credential=credential)
        secret = client.get_secret("azure-openai-key")
        return secret.value

def get_openai_endpoint() -> str:
    return os.environ["AZURE_OPENAI_ENDPOINT"]