# Send a daily Brussels Playbook audio feed to your email

Some years ago, Politico.eu has decided to stop providing an audio feed of their Brussels Playbook to various podcasting apps.

As a consequence, because of large inconvenience, I wrote this `Azure Function` which extract the first article from <https://www.politico.eu/newsletter/brussels-playbook/>, and then extracts Amazon Polly audio file.
Then, it is being forwarded to my email account....on a demand, based on HTTP request to Azure function endpoint.


## How to setup it up for yourself?

Requirements:

- Azure Cloud account
- Azure CLI
- Azure Function CLI <https://github.com/Azure/azure-functions-core-tools>
- Azure Storage resource
- Azure Function resource - will be created using Az CLI


1. Fork this repo
2. In `__init__.py` adjust `send_us_playbook_url` parameters for your emails, and sendgrid api key.
2.2. Generate Sendgrid key if you need it (you will if using sendgrid SaaS)
3. Setup azure account

```shell
az login

```


## Estimated Costs


## Deployment

<https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python#publishing-to-azure>

<https://docs.microsoft.com/en-us/azure/azure-functions/functions-deployment-technologies>

```
# remote
func azure functionapp publish <APP_NAME>

# local
func azure functionapp publish <APP_NAME> --build local
```
