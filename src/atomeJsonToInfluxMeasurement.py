#!/usr/bin/python3
# -*- coding: utf-8 -*-

import iso8601
import json
import re

# ##############################################################################
# ##############################################################################
#
#	Logging configuration
#
import logging

from influxdb.InfluxdbMeasurement import InfluxdbMeasurement

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# ##############################################################################
# ##############################################################################

C_MEASUREMENTNAME_HISTORY='atome_history'
C_MEASUREMENTNAME_LIVE='atome_live'

# ##############################################################################
# ##############################################################################

def fromGraphData(pJsonResponse):
	# print(json.dumps(pJsonResponse, indent=4, sort_keys=True))

	retval	= ''

	# Get data from JSON response
	lQueryPeriod	= pJsonResponse[ "query_params" ]["period"]
	lJsonData	= pJsonResponse["data"]

	# Count measurements to prepare iterating over them
	lMeasurementsCount	= len(lJsonData)
	if lMeasurementsCount == 0:
		log.warning(
			"No measurement in response! response:\n%s",
			pJsonResponse
		)
	else:
		log.debug(
			"Found %d measurements in JSON response.",
			lMeasurementsCount
		)

	# Iterate over measurements and generate Line Protocol strings
	lMeasurementNbr	= 0
	while lMeasurementNbr < lMeasurementsCount:

		# Get JSON data for the processed measurement
		lMeasurementJson	= lJsonData[lMeasurementNbr]
		log.debug("JSON data for measurement %d:\n%s",
			lMeasurementNbr,
			json.dumps(
				lMeasurementJson,
				indent=4,
				# sort_keys=True
				sort_keys=False
			)
		)

		# Build tags dictionnary
		lTagsCommonDict	= {
			"period"	:	lQueryPeriod
		}

		#
		# Build fields dictionnary
		#
		lFieldsDict	= {}


		# Set fields from root structure
		lFieldsDict["totalConsumption"] \
			= lMeasurementJson["totalConsumption"]


		# Set fields from "consumption" sub-struct
		lConsumptionDict	= __jsonConsumption_toDict( 
						lMeasurementJson["consumption"]
					)

		for lCodeKey in lConsumptionDict:
			for lElementKey in lConsumptionDict[lCodeKey]:
				lFieldKey	= ""
				lFieldKey	+= "consumption_"
				lFieldKey	+= lCodeKey + "_"
				lFieldKey	+= lElementKey
				lFieldsDict[lFieldKey] \
					= lConsumptionDict[lCodeKey][lElementKey]

		# Retrieve the measurement's timestamp
		lTimestampRFC3339	= lMeasurementJson["time"]
		lTimestampObj	= iso8601.parse_date(lTimestampRFC3339)
		lTimestampEpoch_s	= lTimestampObj.timestamp()
		lTimestampEpoch_ns	= int(lTimestampEpoch_s * 1000 * 1000 * 1000)

		
		#
		# Generate the Line Protocol string
		#

		# Instanciate the measurement
		lMeasurement	= InfluxdbMeasurement(
			pName	= C_MEASUREMENTNAME_HISTORY,
			pTagsCommonDict	= lTagsCommonDict
		)

		lMeasurement.setTimestamp(lTimestampEpoch_ns)

		lLPString	= lMeasurement.toLineProtocol(
			# pTagsComplementaryDict	=	{
			# 	"tagComp1_key"	:	"tagComp1_value"
			# },
			pFieldsDict	=	lFieldsDict
		)
		# log.debug("lLPString=" + lLPString)
		retval	+= lLPString

		# Increment processed measurements count
		lMeasurementNbr	= lMeasurementNbr + 1


	# log.debug("retval:\n%s", retval)
	return retval

# ##############################################################################
# ##############################################################################
#
##  @brief  Converts the "Live" measurement's JSON data to an
##          InfluxDB Line Protocol data point.
##
##  @note   JSON data is expected to look like this:
##  ~~~~~{json}
##  {
##      "filteredPower": 1337.0,
##      "isConnected": true,
##      "last": 1000.0,
##      "subscribed": 3000.0,
##      "time": "2021-10-01T01:02:03+02:00",
##      "timeLimitBeforePowerFailure": -1
##  }
##  ~~~~~
#
def fromLive(pJsonResponse):
	# print(json.dumps(pJsonResponse, indent=4, sort_keys=True))

	retval	= ''

	# Get data from JSON response
	# lQueryPeriod	= pJsonResponse[ "query_params" ]["period"]
	lJsonData	= pJsonResponse#["data"]


	#
	# Build tags dictionnary
	#
	lTagsCommonDict	= {
		# "period"	:	lQueryPeriod
	}


	#
	# Build fields dictionnary
	#
	lFieldsDict	= {}

	for lKey in lJsonData:
		# The "time" node is not considered as a LineProtocol field.
		if lKey == "time":
			# log.debug("Found time")
			continue
		else:
			lFieldsDict[lKey]	= lJsonData[lKey]


	# Retrieve the measurement's timestamp
	lTimestampRFC3339	= lJsonData["time"]
	lTimestampObj	= iso8601.parse_date(lTimestampRFC3339)
	lTimestampEpoch_s	= lTimestampObj.timestamp()
	lTimestampEpoch_ns	= int(lTimestampEpoch_s * 1000 * 1000 * 1000)


	#
	# Generate the Line Protocol string
	#

	# Instanciate the measurement
	lMeasurement	= InfluxdbMeasurement(
		pName	= C_MEASUREMENTNAME_LIVE,
		pTagsCommonDict	= lTagsCommonDict
	)

	lMeasurement.setTimestamp(lTimestampEpoch_ns)

	lLPString	= lMeasurement.toLineProtocol(
		# pTagsComplementaryDict	=	{
		# 	"tagComp1_key"	:	"tagComp1_value"
		# },
		pFieldsDict	=	lFieldsDict
	)
	# log.debug("lLPString=" + lLPString)
	retval	+= lLPString


	# log.debug("retval:\n%s", retval)
	return retval

# ##############################################################################
# ##############################################################################

def	__jsonConsumption_toDict(pConsumptionJson : dict):
	"""
	Makes the "consumption" structure more readable for the database.

	Received data contains a "consumption" structure where several related
	fields are suffixed by a common number,
	eg. "code1, priceindex1, code2, priceindex2, [...]".
	These usually specify various pricings.
	To make things more readable in the database, this function removes the
	suffix of a data "group" and moves values into a sub-structure named
	after the "code" item.

	For (pseudo-code) example:
	```
	consumption {
		code1="HC"
		bill1=42
		code2="HP"
		bill2=404
	}
	```
	becomes:
	```
	{
		"HC" {
			bill=42
		},
		"HP" {
			bill=404
		}
	}
	```
	"""

	lOutput	= {}

	lGroupNbr	= 1
	# raise Exception("Note: pConsumptionJson type:" + pConsumptionJson.__class__.__name__)
	while "code" + str(lGroupNbr) in pConsumptionJson:
		# log.debug("Group %d exists.", lGroupNbr)

		# Get the code
		lCode	= pConsumptionJson["code" + str(lGroupNbr)]
		lOutput[lCode]	= {} # Create code's root element

		# Find all related values
		for lKey in pConsumptionJson.keys():
			# log.debug("Processing key '%s'", lKey)
			if get_trailing_number(lKey) != lGroupNbr:
				continue
			else:
				# Remove the group number from the key
				lKeyStripped	= re.sub( 
					str(lGroupNbr)+ '$',
					'',
					lKey
				)
				
				# Add key/value to the related section
				lOutput[lCode][lKeyStripped] \
					= pConsumptionJson[lKey]

		# Increment processed group number
		lGroupNbr	= lGroupNbr + 1

	# log.debug("lOutput:\n%s",
	# 	json.dumps(
	# 		lOutput,
	# 		indent=4,
	# 		# sort_keys=True
	# 		sort_keys=False
	# 	)
	# )
	return lOutput

# ##############################################################################
# ##############################################################################

def get_trailing_number(pString:str):
	m	= re.search(r'\d+$', pString)

	if m:
		return int(m.group())
	else:
		return None

# ##############################################################################
# ##############################################################################