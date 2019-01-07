#
# CultureMesh Users API
#

from .client import Request


def get_user(client, userId):
	"""
	:param client: the CultureMesh API client
	:param userId: The id of the user to return.

	Returns JSON of user.
	"""
	url = '/user/%s' % str(userId)
	return client._request(url, Request.GET)
