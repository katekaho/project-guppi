
# Google compute initial configuration instructions

 If Google api client is not installed on your machine run:

    pip install --upgrade google-api-python-client
 
1.  Go to the [google cloud console](https://console.cloud.google.com/) and create an account or sign onto your existing one.

2.  Go to the [cloud resource manager](https://console.cloud.google.com/cloud-resource-manager) and select or create a Google Cloud Platform project 
**NOTE: GUPPI will only work if your google account has only one project associated with it**

3.  Ensure that [billing is enabled](https://cloud.google.com/billing/docs/how-to/modify-project) for your Google Cloud Platform Project

4.  Install the [Cloud SDK](https://cloud.google.com/sdk/)

5.  Authenticate your account on your machine
    
    ``gcloud auth application-default login``

6.  Follow google documentation [HERE](https://cloud.google.com/apis/docs/enable-disable-apis?hl=en&ref_topic=6262490&visit_id=636909616876722358-4171110160&rd=1) to enable the Google Cloud Storage API and Cloud Resource Manager API

7.  [Create a storage bucket](https://cloud.google.com/storage/docs/creating-buckets) and note the bucket name for later

8.  Create a [service account for authentication](https://console.cloud.google.com/projectselector/apis/credentials/serviceaccountkey?supportedpurview=project)
    1.  From the Service account list, select **New service account.**
    2.  In the **Service account name field**, enter a name.
    3.  From the **Role list,** select **Project > Owner.**
    4.  Click **Create.** This should download a JSON key
    5.  Move this key file into the ``googleCredentials`` folder found in ``project-guppi/src/plugins/GoogleService``, this file should end with .json

9.  Follow [these instructions](https://cloud.google.com/compute/docs/instances/adding-removing-ssh-keys#project-wide) to create and add a public SSH key to your project. 
Note: When generating the rsa key, ensure that the key comment is the same as your email, with ``. @ -`` symbols replaced with underscores, for example ``user_lastname_gmail_com``.
Make sure that you go to [project metadata](https://console.cloud.google.com/compute/metadata/sshKeys) and save the public RSA key to your SSH keys

10. Save the private SSH key as gc_rsa.pem and move it into ``project-guppi/src/plugins/GoogleService`` in guppi.

11.  Reload the ``%guppi cloud`` command in Jupyter Notebook
