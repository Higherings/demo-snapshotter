import boto3
import click    #module to work with parameters
#import sys #for arguments as input

session = boto3.Session(profile_name='demo_python')
ec2 = session.resource('ec2')

def filter_instances(proyecto):
    instances = []
    if proyecto:
        filters = [{'Name':'tag:proyecto', 'Values':[proyecto]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

@click.group()
def instances():
    """Commands for instances"""

#@click.command()    #wrapper
@instances.command('list')
@click.option('--proyecto', default=None, help="Only instances for project (tag proyecto:<name>)")
def list_instances(proyecto):
    "List Instances"    #doc string
    instances = filter_instances(proyecto)

    for i in instances:
        tags = { t['Key']:t['Value'] for t in i.tags or [] }
        print (', '.join((i.id, i.instance_type, i.placement['AvailabilityZone'], i.state['Name'], i.public_dns_name, tags.get('proyecto', '<no proyecto>'))))
    return

@instances.command('stop')
@click.option('--proyecto', default=None, help="Only instances for project (tag proyecto:<name>)")
def stop_instances(proyecto):
    "Stop Instances"
    instances = filter_instances(proyecto)
    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()
    return

@instances.command('start')
@click.option('--proyecto', default=None, help="Only instances for project (tag proyecto:<name>)")
def stop_instances(proyecto):
    "Start Instances"
    instances = filter_instances(proyecto)
    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()
    return


if __name__ == '__main__':
    #print(sys.argv) #sys.argv will hace a list of strings with the parameters
    instances()

