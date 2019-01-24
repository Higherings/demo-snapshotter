##HOW-TO run: pipenv run python shotter/shotter.py instances snapshot --proyecto=python_demo

import boto3
import botocore
import click    #module to work with parameters
#import sys #for arguments as input

session = boto3.Session(profile_name='demo_python') #profile_name debe ser igual a --profile cuando se corre aws config
ec2 = session.resource('ec2')

def filter_instances(proyecto):
    instances = []
    if proyecto:
        filters = [{'Name':'tag:proyecto', 'Values':[proyecto]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

@click.group() #Will group volumes and instances groups
def cli():
    """Shotter manages snapshots"""

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')
@click.option('--proyecto', default=None, help="Only snapshots for project (tag proyecto:<name>)")
def list_snapshots(proyecto):
    "List Snapshots"    #doc string
    instances = filter_instances(proyecto)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((s.id, v.id, i.id,s.state,s.progress, s.start_time.strftime("%c"))))
    return


@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@volumes.command('list')
@click.option('--proyecto', default=None, help="Only volumes for project (tag proyecto:<name>)")
def list_volumes(proyecto):
    "List Volumes"    #doc string
    instances = filter_instances(proyecto)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((v.id, i.id,v.state,str(v.size)+"GiB", v.encrypted and "Encrypted" or "Not Encrypted")))
    
    return

@cli.group('instances')  #here we define a group to work with commands for instances
def instances():
    """Commands for instances"""

#@click.command()    #wrapper

@instances.command('snapshot', help="Create a snaphot of all volumes")
@click.option('--proyecto', default=None, help="Only instances for project (tag proyecto:<name>)")
def create_snapshots(proyecto):
    "Create Snapshots"    #doc string
    instances = filter_instances(proyecto)
    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()
        i.wait_until_stopped()  #waits until the instance is stopped
        for v in i.volumes.all():
            print("     Creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by Shotter Snaps")
        print("Starting {0}...".format(i.id))
        i.start()
        i.wait_until_running()

    print("All done!")
    return




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
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print("Could not stop {0} ".format(i.id)+str(e))
            continue
    return

@instances.command('start')
@click.option('--proyecto', default=None, help="Only instances for project (tag proyecto:<name>)")
def stop_instances(proyecto):
    "Start Instances"
    instances = filter_instances(proyecto)
    for i in instances:
        print("Starting {0}...".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print("Could not start {0} ".format(i.id)+str(e))
            continue

    return


if __name__ == '__main__':
    #print(sys.argv) #sys.argv will hace a list of strings with the parameters
  cli()

