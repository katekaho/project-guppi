#%%
import boto3
from ipywidgets import widgets
button = widgets.Button(description = "generate key pair")
display(button)
def on_button_clicked(b):
    print("clicked")
    ec2 = boto3.resource('ec2')

    # create a file to store the key locally
    outfile = open('ec2-keypair1.pem','w')

    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(KeyName='ec2-keypair1')

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    print(KeyPairOut)
    outfile.write(KeyPairOut)
button.on_click(on_button_clicked)