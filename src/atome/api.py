#!/usr/bin/python3
# -*- coding: utf-8 -*-

import	os
import	requests
import	sys
from requests.models import ReadTimeoutError

from rx import return_value

from	.	import	config
from	.exceptions	import	AtomeException, CollectException
from	.exceptions	import	LoginException


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

API_BASE_URI	= 'https://esoftlink.esoftthings.com'
API_ENDPOINT_LOGIN	= '/api/user/login.json'
API_ENDPOINT_GRAPH	= '/graph-query-last-consumption'

C_COOKIE_NAME		= 'PHPSESSID'

# ##############################################################################
# ##############################################################################

def	init():
	log.debug("Initialize config.")

	if config.read() is not True:
		log.warning("Current credentials are not valid!")
		config.create(
			"default_atome_login",
			"default_atome_password",
			"default_deviceName"
		)
		config.save()
	else:
		log.debug("Credentials read success.")

# ##############################################################################
# ##############################################################################
#
##  @brief  This function logs into the Atome API by retrieving a session token.
#
def login():

	try:
		# We already have a session token - then we are already logged.
		if	config.getSessionToken() is not None \
		and	config.getUserId() is not None \
		and	config.getUserReference() is not None:

			log.debug("Already logged in.")
			return True


	except Exception as e:
		log.info("Can't retrieve session identifiers: " + str(e) )


	#
	# Login
	#
	log.info("Try to login...")
	try:
		log.info("Using login '%s'", config.getLogin())


		# Login the user into the Atome API.
		payload = {
			"email": config.getLogin(),
			"plainPassword": config.getPassword()
		}

		req = requests.post(
			API_BASE_URI + API_ENDPOINT_LOGIN,
			json=payload,
			headers={"content-type":"application/json"}
		)
		response_json = req.json()
		session_token = req.cookies.get(C_COOKIE_NAME)
		log.debug("session_token=" + str(session_token) )

		if session_token is None:
			raise LoginException("Login unsuccessful. Check your credentials.")

		# Store session token
		config.setSessionToken(str(session_token))

		# Store user IDs
		config.setUserId( str(response_json['id']) )
		config.setUserReference(
			response_json['subscriptions'][0]['reference']
		)

		return True


	except LoginException as exc:
		log.error(exc)
		# sys.exit(1)
		raise
	except Exception as e:
		log.error("An exception occured: " + str(e) )
		raise
		# return False

# ##############################################################################
# ##############################################################################

def getGraphData(pPeriod:str='month'):
	# We send the session token so that the server knows who we are
	cookie = {
		C_COOKIE_NAME: config.getSessionToken()
	}

	params = {
		# 'period': 'day', #< ok mais foireux ?
		# 'period': 'month', #< ok
		# 'period': 'year', #< ok
		'period': pPeriod,
		'objective': 'false'
	}

	url	= API_BASE_URI
	url	+= '/' + config.getUserId()
	url	+= '/' + config.getUserReference()
	url	+= API_ENDPOINT_GRAPH

	req_json = _request_get(
		pUrl	= url,
		pCookies	= cookie,
		pParams	= params
	)

	retval	= req_json
	retval[ "query_params" ]	= {}
	retval[ "query_params" ]["period"]	= pPeriod
	return retval

# ##############################################################################
# ##############################################################################

def getLiveData():#pPeriod:str='day'):
	# We send the session token so that the server knows who we are
	lCookies = {
		C_COOKIE_NAME: config.getSessionToken()
	}

	lParams = {
		# 'period': 'day',
		# 'period': 'month',
		# 'period': 'year',
		# 'period': pPeriod,
		'objective': 'false'
	}

	lUrl	= API_BASE_URI
	lUrl	+= '/api/subscription'
	lUrl	+= '/' + config.getUserId()
	lUrl	+= '/' + config.getUserReference()
	lUrl	+= "/measure/live.json"


	retvalJson	= _request_get(
		pUrl	= lUrl,
		pCookies	= lCookies,
		pParams	= lParams
	)

	return retvalJson

# ##############################################################################
# ##############################################################################

def	_request_get(
		pUrl:str,
		pCookies:dict={},
		pParams=None,
		pTimeout_s	= 30
	):

	log.debug(
		"URL='%s', params='%s', cookies='%s'",
		pUrl,
		str(pParams),
		str(pCookies)
	)


	try:
		req = requests.get(
			url	= pUrl,
			cookies	= pCookies,
			params	= pParams,
			allow_redirects=False,
			timeout	= pTimeout_s
		)
	except requests.ReadTimeout as e:
		log.error("Read timeout.")
		raise CollectException("Read timeout. " + str(e) )

	except Exception as e:
		log.error("An exception occured: " + str(e) )
		raise CollectException("An exception occured: " + str(e) )


	if req.status_code == 302:
		# os.remove(COOKIE_FILE)
		config.clearSessionToken()
		raise LoginException("Session token expired.")

	elif req.status_code == 403:
		config.clearSessionToken()
		raise LoginException("403 Forbidden.")

	elif req.status_code != 200:
		lErrorMsg	= "Can't get data from Atome ; reason: " \
			+ str(req.status_code) + "/" + req.reason

		log.error( lErrorMsg )
		config.clearSessionToken()
		raise AtomeException( lErrorMsg )

	else:
		retval	= req.json()
		return retval

# ##############################################################################
# ##############################################################################
