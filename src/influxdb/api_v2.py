#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

from	.	import	config

from	influxdb_client	import	InfluxDBClient, Point, WritePrecision
from	influxdb_client.client.write_api	import SYNCHRONOUS

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

def	init():
	log.debug("Initialize config.")

	if config.read() is not True:
		log.warning("Config can't be read!")
		config.create()
		config.save()
	else:
		log.debug("Config read success.")

# ##############################################################################
# ##############################################################################

def	writeLP(pDataLineProtocol_str:str):

	# You can generate a Token from the "Tokens Tab" in the UI
	lInfluxdbUrl	= "http://" + config.getHost() + ":" + config.getPort()
	lInfluxToken = config.getToken()

	client = InfluxDBClient(
		url=lInfluxdbUrl,
		token=lInfluxToken
	)

	write_api = client.write_api(write_options=SYNCHRONOUS)

	lOrg = config.getOrg()
	lBucket = config.getBucket()
	write_api.write(
		lBucket,
		lOrg,
		# "test_connect ok=1"
		pDataLineProtocol_str
	)
	# # establish a connection
	# lClient = InfluxDBClient(
	# 	url=lUrl,
	# 	token=lToken,
	# 	org=lOrg
	# )

	# # instantiate the WriteAPI
	# lWrite_api = lClient.write_api()

	# # Write data points
	# # lWrite_api.write(
	# # 	lBucket,
	# # 	lOrg,
	# # 	pDataLineProtocol_str
	# # )
	# lResult	= lWrite_api.write(
	# 	lBucket,
	# 	lOrg,
	# 	["test_connect ok='1'"]
	# )

	# log.debug("lResult=" + str(lResult) )

# ##############################################################################
# ##############################################################################