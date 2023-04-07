

class EC2:
    def __int__(self, client):
        self._client = client
        """:type:pyboto3.ec2"""

    def create_key_pair(self, key_name):
        return self._client.create_key_pair(KeyName=key_name)

    def create_security_grp(self,  grp_name, description, vpc_id):
        print("creating security group")
        return self._client.create_security_group(
            GroupName=grp_name,
            Description=description,
            VpcId=vpc_id
        )

    def add_inbound_rule(self, security_grp_id):
        print("Adding inbound rule for the security group")
        return self._client.authorize_security_group_ingress(
            GroupId=security_grp_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort':80,
                    'ToPort':80,
                    'IpRanges':[{'CidrIp:0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp:0.0.0.0/0'}]
                }
            ]
        )

    def launch_ec2_instance(self, image_id, key_name, min_count, max_count, instance_type, security_grp_id, subnet_id, user_data):
        print("Launching EC2 instance ")
        return self._client.run_instances(
            ImageId=image_id,
            KeyName=key_name,
            MinCount=min_count,
            MaxCount=max_count,
            InstanceType=instance_type,
            SecurityGroupIds=security_grp_id,
            SubnetId=subnet_id,
            User_data=user_data

        )


