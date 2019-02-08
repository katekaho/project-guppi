#%%
import boto3
ec2 = boto3.resource('ec2')

# create a file to store the key locally
outfile = open('ec2-keypair2.pem','w')

# call the boto ec2 function to create a key pair
key_pair = ec2.create_key_pair(KeyName='ec2-keypair2')

# capture the key and store it in a file
KeyPairOut = str(key_pair.key_material)
print(KeyPairOut)
outfile.write(KeyPairOut)


#%%
# create a new EC2 instance
instances = ec2.create_instances(
     ImageId='ami-0799ad445b5727125',
     MinCount=1,
     MaxCount=2,
     InstanceType='t2.micro',
     KeyName='ec2-keypair2'
 )
