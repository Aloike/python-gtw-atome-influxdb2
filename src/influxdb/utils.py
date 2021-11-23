#!/usr/bin/python3
# -*- coding: utf-8 -*-

import	numbers

# ##############################################################################
# ##############################################################################
#
#	Logging configuration
#
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# ##############################################################################
# ##############################################################################


def	fieldsDict_toLineProtocolString(pFieldsDict:dict):
	"""Converts a fields dictionnary to a valid LineProtocol string."""

	retval	=	''

	for lFieldName in pFieldsDict:
		lFieldValue = pFieldsDict[lFieldName]

		if retval != '':
			retval	+= ','

		retval	+= lFieldName
		retval	+= '='
		if isinstance(lFieldValue, numbers.Number):
			# If the field value is considered a number, write it directly
			retval	+= str(lFieldValue)
		else:
			# Otherwise, wrap the field inside double quotes to consider it as
			# a string.
			retval	+= "\"" + str(lFieldValue) + "\""


	return retval

# ##############################################################################
# ##############################################################################

def	tagsDict_toLineProtocolString(pTagsDict:dict):
	"""Converts a tags dictionnary to a valid LineProtocol string."""

	retval	=	''

	for lTagName in pTagsDict:
		lTagValue = pTagsDict[lTagName]

		# See https://docs.influxdata.com/influxdb/v1.7/write_protocols/line_protocol_tutorial/#special-characters
		if type(lTagValue) == str:
			lTagValue	=	lTagValue.replace(",", "\\,")
			lTagValue	=	lTagValue.replace("=", "\\=")
			lTagValue	=	lTagValue.replace(" ", "\\ ")

		if retval != '':
			retval	+= ','

		retval	+= lTagName
		retval	+= '='
		retval	+= str(lTagValue) # Tags are always strings

	return retval

# ##############################################################################
# ##############################################################################