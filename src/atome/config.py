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
log.setLevel(logging.INFO)

# ##############################################################################
# ##############################################################################

C_KEY_ATOMESECTION	=	"atome"
C_KEY_ATOME_LOGIN	=	"atome_login"
C_KEY_ATOME_PASSWORD	=	"atome_password"
C_KEY_ATOME_SESSION_TOKEN	=	"session_token"
C_KEY_ATOME_USER_ID	=	"user_id"
C_KEY_ATOME_USER_REFERENCE	=	"user_reference"

# ##############################################################################
# ##############################################################################

##  @brief  This dictionnary contains configuration parameters of this app.
g_atome_config	=	{}

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

def	clearSessionToken():
	log.info("Removing session token.")

	g_atome_config.pop( C_KEY_ATOME_SESSION_TOKEN )
	save()

# ##############################################################################
# ##############################################################################
#
##  @brief  Create a default configuration.
#
def create(pLogin, pPassword, pDeviceName):

	log.info("Creating default config.")

	global	g_atome_config
	g_atome_config	=	{}
	try:
		g_atome_config[C_KEY_ATOME_LOGIN]	= pLogin
		g_atome_config[C_KEY_ATOME_PASSWORD]	= pPassword


	except configp.NoSectionError:
		exit()

	return g_atome_config

# ##############################################################################
# ##############################################################################

def	exists():
	global	g_atome_config

	if not g_atome_config:
		return False
	else:
		return True

# ##############################################################################
# ##############################################################################

def	getLogin():
	return	g_atome_config[C_KEY_ATOME_LOGIN]

# ##############################################################################
# ##############################################################################

def	getPassword():
	return	g_atome_config[C_KEY_ATOME_PASSWORD]

# ##############################################################################
# ##############################################################################

def	getSessionToken():
	return	g_atome_config[C_KEY_ATOME_SESSION_TOKEN]

# ##############################################################################
# ##############################################################################

def	getUserId():
	return	g_atome_config[C_KEY_ATOME_USER_ID]

# ##############################################################################
# ##############################################################################

def	getUserReference():
	return	g_atome_config[C_KEY_ATOME_USER_REFERENCE]

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
	global	g_atome_config
	g_atome_config	=	{}
	try:
		# lEndpoint	= __endpoint()
		_ = lCfgFile.has_section(C_KEY_ATOMESECTION)

		for lKey in dict(lCfgFile.items(C_KEY_ATOMESECTION)).keys():
			log.debug("key:" + lKey )
			g_atome_config[lKey]	=	lCfgFile.get(C_KEY_ATOMESECTION, lKey)


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
	if lCfgParser.has_section(C_KEY_ATOMESECTION) is False:
		lCfgParser.add_section(C_KEY_ATOMESECTION)


	# Add the configuration key/value pairs into the correponding section
	for lKey in g_atome_config.keys():
		lCfgParser.set(	
			C_KEY_ATOMESECTION,
			lKey,
			g_atome_config.get(lKey) 
		)

	#    with open(lCfgFileName, "ab") as authFile:
	# with open(lCfgFileName, "a") as authFile:
	with open(_config_filePath(), "w") as configFile:
		lCfgParser.write(configFile)

# ##############################################################################
# ##############################################################################

def	setSessionToken(pToken: str):
	g_atome_config[C_KEY_ATOME_SESSION_TOKEN]	= pToken
	save()

# ##############################################################################
# ##############################################################################

def	setUserId(pValue: str):
	g_atome_config[C_KEY_ATOME_USER_ID]	= pValue
	save()

# ##############################################################################
# ##############################################################################

def	setUserReference(pValue: str):
	g_atome_config[C_KEY_ATOME_USER_REFERENCE]	= pValue
	save()

# ##############################################################################
# ##############################################################################

def	toDict():
	return g_atome_config

# ##############################################################################
# ##############################################################################

def	toJson():
	return json.dumps(g_atome_config, indent = 4)

# ##############################################################################
# ##############################################################################
