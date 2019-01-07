#
# CultureMesh Networks API
#

from .client import Request


def get_network(client, networkId):
    """
    :param client: the CultureMesh API client
    :param networkId: The id of the network to return.

    Returns JSON of network.
    """
    url = 'network/%s' % str(networkId)
    return client._request(url, Request.GET)
