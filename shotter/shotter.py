import boto3
import click    #module to work with parameters
#import sys #for arguments as input

session = boto3.Session(profile_name='demo_python')
ec2 = session.resource('ec2')

@click.command()    #wrapper
def list_instances():
    "List Instances"    #doc string
    for i in ec2.instances.all():
        print (', '.join((i.id, i.instance_type, i.placement['AvailabilityZone'], i.state['Name'], i.public_dns_name)))
    return

if __name__ == '__main__':
    #print(sys.argv) #sys.argv will hace a list of strings with the parameters
    list_instances()

