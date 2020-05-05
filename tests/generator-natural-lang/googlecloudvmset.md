# Steps:

1. Setup a google account with Google Cloud
2. Create a project
3. Set permission for create on compute engine in the project
3. create a service account file and link to json in cloudmesh yaml file 
https://cloud.google.com/docs/authentication/production?hl=en_US
3. Create a storage location using google storage
https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-code_samples
4. Install the google cloud sdk 
https://cloud.google.com/compute/docs/tutorials/python-guide
5. Install the google cloud api client library 
https://cloud.google.com/apis/docs/client-libraries-explained 
6. Write a startup script for your vm





## Azure
https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal
Credentials:
app-name: vm-creation-example
auth url:https://andyvmcreateexample.com/auth

app (client) ID: 8db85342-7efd-433c-aeba-d175ae4d4404
directory (tenant) id: 398e5475-e850-4239-ba0d-62ddc3e644ff
object ID: 38224a7e-79e0-4642-b765-2bf731d296ad
client-secret: w[f7o=[dKKeSn?VxF3iNoZDW3ctMmd3G
subscription id:4513afc9-4159-49d0-aa1d-0a2a0ab9933c

when creating a vm in the portal the network interface is set up for you
but if you do it programmatically you have to set it up.
