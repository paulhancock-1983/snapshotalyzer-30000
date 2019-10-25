import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    instance = []

    if project:
         filters = [{'Name':'tag:Project', 'Values':[project]}]
         instances = ec2.instances.filter(Filter=filters)
    else:
         instances = ec2.instances.all()

    return instances

@click.group()
def instances():
    """Commands for instances"""
@instances.command('list')
@click.option('--project', default=None,
help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List ec2 instance"

    instances = filter_instances(project)

    for i in ec2.instances.all():
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>')
            )))

        return

@instances.command('stop')
@click.option('--project', default=None)
def stop_instances(project):
    "start EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("stopping {0}...".format(i.id))
        i.stop()

    return


if __name__ == '__main__':
    instances()
