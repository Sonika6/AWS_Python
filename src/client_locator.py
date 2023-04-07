import boto3


class ClientLocator:
    def __init__(self, client):
        self._client = boto3.client(client, region_name="ap-south-1")

    def get_client(self):
        return self._client


class EC2Client(ClientLocator):
    def __init__(self):
        super().__init__('ec2')

    def __int__(self):
        return self._client.create_vpc(
            CidrBlock='10.0.0.0/16'
        )

