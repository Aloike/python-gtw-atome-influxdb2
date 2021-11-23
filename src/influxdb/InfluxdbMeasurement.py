#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
##  @file
##
##  @see    Line Protocol syntax: https://docs.influxdata.com/influxdb/cloud/reference/syntax/line-protocol/
#

from	influxdb.utils	import	fieldsDict_toLineProtocolString, tagsDict_toLineProtocolString

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

class	InfluxdbMeasurement:
	"""This class represents an InfluxDB measurement."""

	# ----------------------------------------------------------------------
	# ----------------------------------------------------------------------

	def __init__(self, pName:str, pTagsCommonDict:dict={}):
		"""Constructor"""

		self._measurementName	=	pName
		self._tagsCommon_dict	=	pTagsCommonDict
		self._timestamp	=	None

		pass

	# ----------------------------------------------------------------------
	# ----------------------------------------------------------------------

	def	setTimestamp(self, pTimestamp_ns: int):
		self._timestamp_ns	= pTimestamp_ns

	# ----------------------------------------------------------------------
	# ----------------------------------------------------------------------

	def	timestamp(self):
		return self._timestamp_ns

	# ----------------------------------------------------------------------
	# ----------------------------------------------------------------------

	def	toLineProtocol(self, pFieldsDict:dict, pTagsComplementaryDict:dict={}):
		"""
		This method outputs a string representing the measurement as an
		InfluxData Line Protocol string.
		"""

		# Merge given tags with common tags
		# lTags	= __tags_commonDict() | pTagsDict
		lTags	=	{
			**self._tagsCommon_dict,
			**pTagsComplementaryDict
		}

		# Encode the tags dictionnary to a string
		lTagsStr	= tagsDict_toLineProtocolString(lTags)

		# Encode the fields dictionnary to a string
		lFieldsStr	= fieldsDict_toLineProtocolString(pFieldsDict)


		#
		#	Generate the output line
		#

		# Add measurement name
		lOutput	= self._measurementName

		# Add tags
		if lTagsStr != '':
			lOutput	+= ',' + lTagsStr

		# Add fields
		lOutput	+= ' '
		lOutput	+= lFieldsStr

		# Add the timestamp if one is defined
		if self.timestamp() is not None:
			lOutput	+= ' '
			lOutput	+= '%d' % self.timestamp()

		# Add end of line
		lOutput	+= "\n"

		# return the line
		return lOutput

# ##############################################################################
# ##############################################################################
