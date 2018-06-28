# -*- coding:utf-8 -*-
import boto3
import sys


class Create_err(Exception):
    """Logged invalid message."""

    def __init__(self, err_msg):
        self.err_msg = err_msg
        pass


class EC2():
    def __init__(self):
        self.create_instance_args = None
        self.ec2_resource = boto3.resource('ec2')
        self.instances = list(self.ec2_resource.instances.all())
        self.runinstances = list(self.ec2_resource.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]))

    def create(self, **kwargs):

        if not kwargs.get("ImageId"):
            raise Create_err("ImageId is null")
        if not kwargs.get("MinCount"):
            kwargs['MinCount'] = 1
        if not kwargs.get("MaxCount"):
            kwargs['MaxCount'] = 1
        if kwargs.get("MaxCount") < kwargs.get("MinCount"):
            raise Create_err(
                "MaxCount:%s, MinCount:%s, MinCount > MaxCount?" % (kwargs.get("MaxCount"), kwargs.get("MinCount")))

        self.create_instance_args = kwargs
        try:
            new_instances = self.ec2_resource.create_instances(**self.create_instance_args)
        except Exception as e:
            raise Create_err(e.message)
        if new_instances:
            self.instances = self.instances + new_instances

        return (new_instances, self.instances)

    def get_ec2_status(self, instances_id=None):
        pass

#
# if __name__ == '__main__':
#     try:
#         ec2_instances = EC2()
#     except InvalidParms as e:
#         print e.err_msg
#
#     #ec2instances = ec2_instances.create(ImageId='ami-02de0cb5595f2050d', MinCount=1, MaxCount=1, InstanceType='t2.micro',KeyName='My_key', SecurityGroups=['default', ], BlockDeviceMappings=[{'DeviceName': '/dev/sda1','Ebs':{'VolumeType':'standard'}}])
#     for instance in ec2_instances.instances:
#         if instance.state.get("Name") == 'running':
#             print instance
