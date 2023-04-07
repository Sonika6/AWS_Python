
class VPC:
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.ec2 """

    def create_vpc(self):
        return self._client.create_vpc(
            CidrBlock='10.0.0.0/16'
        )

    def add_tag(self, resource_id, resource_name):
        return self._client.create_tags(
            Resources=[resource_id],
            Tags=[{
                'Key': 'Name',
                'Value': resource_name
            }]
        )

    def create_ig(self):
        print("Creating Internet gateway...")
        return self._client.create_internet_gateway()

    def attach_igw_to_vpc(self, vpc_id, igw_id):
        print("Attaching internet gateway")
        return self._client.attach_internet_gateway(
            InternetGatewayId=igw_id,
            VpcId=vpc_id
        )

    def create_subnet(self, vpc_id, cidr):
        print("Creating a subnet")
        return self._client.create_subnet(
            VpcId=vpc_id,
            CidrBlock=cidr
        )

    def create_route_table(self, vpc_id):
        print("Creating a route table")
        return self._client.create_route_table(
            VpcId=vpc_id
        )

    def create_igw_route_to_public_route_table(self, rtb_id, igw_id):
        print("Adding IGW route to route table")
        return self._client.create_route(
            RouteTableId=rtb_id,
            GatewayId=igw_id,
            DestinationCidrBlock='0.0.0.0/0'
        )

    def associate_subnet_to_rtb(self, rtb_id, subnet_id):
        print("Associating subnet to route table")
        return self._client.associate_route_table(
            SubnetId=subnet_id,
            RouteTableId=rtb_id
        )

    def allow_auto_assign_ip_address_for_subnet(self, subnet_id):
        print("Allow auto assign ip address for subnet")
        return self._client.modify_subnet_attribute(
            SubnetId=subnet_id,
            MapPublicIpOnLaunch={'Value': True}
        )


