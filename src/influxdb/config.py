#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import json
import os
import sys

if sys.version_info >= (3, 0):
    import configparser as configp
else:
    import ConfigParser as configp

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

C_KEY_SECTION	=	"influxdb2"
C_KEY_INFLUXDB2_HOST	=	"host"
C_KEY_INFLUXDB2_PORT	=	"port"
C_KEY_INFLUXDB2_ORG	=	"org"
C_KEY_INFLUXDB2_BUCKET	=	"bucket"
C_KEY_INFLUXDB2_TOKEN	=	"token"

# ##############################################################################
# ##############################################################################

##  @brief  This dictionnary contains configuration parameters of this app.
g_influxdb2_config	=	{}

# ##############################################################################
# ##############################################################################

def	_config_filePath():
	lFilename	= ".config.ini"

	# script_dir = os.path.dirname(os.path.realpath(__file__))
	# cfg_file = os.path.join(script_dir, lFilename)

	cfg_file = os.path.join(os.getcwd(), lFilename)

	return cfg_file

# ##############################################################################
# ##############################################################################

# def	clearSessionToken():
# 	log.debug("Remove session token.")

# 	g_influxdb2_config.pop( C_KEY_ATOME_SESSION_TOKEN )
# 	save()

# ##############################################################################
# ##############################################################################
#
##  @brief  Create a default configuration.
#
def 	create(
		pHost:str="localhost",
		pPort:str="8086",
		pOrg:str="example.org",
		pBucket:str="example_bucket",
		pToken:str="example_token"
	):

	log.info("Creating default config.")

	global	g_influxdb2_config
	g_influxdb2_config	=	{}
	try:
		g_influxdb2_config[C_KEY_INFLUXDB2_HOST]	= pHost
		g_influxdb2_config[C_KEY_INFLUXDB2_PORT]	= pPort
		g_influxdb2_config[C_KEY_INFLUXDB2_ORG]		= pOrg
		g_influxdb2_config[C_KEY_INFLUXDB2_BUCKET]	= pBucket
		g_influxdb2_config[C_KEY_INFLUXDB2_TOKEN]	= pToken


	except configp.NoSectionError:
		exit()

	return g_influxdb2_config

# ##############################################################################
# ##############################################################################

def	exists():
	global	g_influxdb2_config

	if not g_influxdb2_config:
		return False
	else:
		return True

# ##############################################################################
# ##############################################################################

def	getBucket():
	return	g_influxdb2_config[C_KEY_INFLUXDB2_BUCKET]

# ##############################################################################
# ##############################################################################

def	getHost():
	return	g_influxdb2_config[C_KEY_INFLUXDB2_HOST]

# ##############################################################################
# ##############################################################################

def	getOrg():
	return	g_influxdb2_config[C_KEY_INFLUXDB2_ORG]

# ##############################################################################
# ##############################################################################

def	getPort():
	return	g_influxdb2_config[C_KEY_INFLUXDB2_PORT]

# ##############################################################################
# ##############################################################################

def	getToken():
	return	g_influxdb2_config[C_KEY_INFLUXDB2_TOKEN]

# ##############################################################################
# ##############################################################################
#
##  @brief  Reads the configuration file and returns a Dictionnary containing
##          configuration values.
#
def read():

	log.debug("Read config.")

	# Create the file parser
	lCfgFile = configp.RawConfigParser()

	# Load the application configuration
	lCfgFileName	= _config_filePath()
	lCfgFile.read(lCfgFileName)


	#
	#	Parse the configuration file
	#
	global	g_influxdb2_config
	g_influxdb2_config	=	{}
	try:
		# lEndpoint	= __endpoint()
		_ = lCfgFile.has_section(C_KEY_SECTION)

		for lKey in dict(lCfgFile.items(C_KEY_SECTION)).keys():
			log.debug("key:" + lKey )
			g_influxdb2_config[lKey] \
				= lCfgFile.get(
					C_KEY_SECTION,
					lKey
				)


	except configp.NoSectionError:
		return False

	except Exception as e:
		log.error("An exception occured: " + str(e) )
		return False


	return True

# ##############################################################################
# ##############################################################################

def	save():

	log.info("Saving current config.")

	# Create the file parser
	lCfgParser	= configp.RawConfigParser()

	# Load the existing application configuration
	lCfgFileName	= _config_filePath()
	lCfgParser.read(lCfgFileName)


	# Set the related configuration section
	if lCfgParser.has_section(C_KEY_SECTION) is False:
		lCfgParser.add_section(C_KEY_SECTION)


	# Add the configuration key/value pairs into the correponding section
	for lKey in g_influxdb2_config.keys():
		lCfgParser.set(	C_KEY_SECTION,
			lKey,
			g_influxdb2_config.get(lKey) 
		)

	with open(_config_filePath(), "w") as configFile:
	# with open(_config_filePath(), "a") as configFile:
		lCfgParser.write(configFile)

# ##############################################################################
# ##############################################################################

def	toDict():
	return g_influxdb2_config

# ##############################################################################
# ##############################################################################

def	toJson():
	return json.dumps(
		g_influxdb2_config,
		indent = 4
	)

# ##############################################################################
# ##############################################################################
