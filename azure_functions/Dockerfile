# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.11-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

RUN curl https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && \
apt-get update && \
ACCEPT_EULA=Y apt-get install -y msodbcsql17
    
COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY common /home/site/wwwroot/common
COPY shared /home/site/wwwroot/shared
COPY helpers /home/site/wwwroot/helpers
COPY function_app.py /home/site/wwwroot
COPY host.json /home/site/wwwroot