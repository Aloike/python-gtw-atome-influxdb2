#!/usr/bin/python3
# -*- coding: utf-8 -*-

from configparser import LegacyInterpolation
from	datetime	import	datetime
from	datetime	import	timedelta
import	json
import	os
import	pause
import	time

import	atome.api
import	atome.config
import	atome.exceptions
import	influxdb.api_v2
import	influxdb.config

import	atomeJsonToInfluxMeasurement


# ##############################################################################
# ##############################################################################
#
#	Logging configuration
#
import	logging

# FORMAT = "%(asctime)s [%(levelname)6s][%(filename)10s +%(lineno)s \t- %(funcName)15s() ] %(message)s"
FORMAT = "%(asctime)s [%(levelname)6s][%(filename)s +%(lineno)s - %(funcName)s() \t] %(message)s"
logging.basicConfig(
	format=FORMAT
	, datefmt='%Y-%m-%dT%H:%M:%S'
)

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# ##############################################################################
# ##############################################################################

def	do_collectHistory(pGraphDataPeriod:str="month"):

	log.info("Collecting data for " + pGraphDataPeriod + "...")
	atome.api.login()


	lJsonData	= atome.api.getGraphData(pGraphDataPeriod)

	# log.info("Values:")
	# print(json.dumps(lJsonData, indent=4, sort_keys=True))


	# Convert Atome data to InfluxDB Line Protocol
	lDataLP	= atomeJsonToInfluxMeasurement.fromGraphData(lJsonData)

	# Write Line Protocol data to InfluxDBv2:
	influxdb.api_v2.writeLP( lDataLP )


	# except Exception as lE:
	# # except LoginException as lE:
	# 	log.critical("An exception occured: " + str(lE) )

# ##############################################################################
# ##############################################################################

def	do_collectLive():

	log.info("Collecting live data...")

	# Login to Atome (if needed)
	atome.api.login()

	# Query data from Atome
	lJsonData = atome.api.getLiveData()
	log.debug(
		"lJsonData:\n%s",
		json.dumps(
			lJsonData,
			indent=4,
			sort_keys=True
		)
	)

	# Convert Atome JSON to InfluxDB Line Protocol
	lDataLP	= atomeJsonToInfluxMeasurement.fromLive(lJsonData)
	log.debug(
		"lDataLP:\n%s",
		lDataLP
	)

	# Write Line Protocol data to InfluxDBv2:
	try:
		influxdb.api_v2.writeLP( lDataLP )

	except Exception as ex:
		log.error(
			"An exception occured while writing to the database:\n"
			+ str(ex)
		)


# ##############################################################################
# ##############################################################################
#
##  @brief  Main routine.
#
def main():

	log.info("Hello, world!")
	log.info("Current workdir: '" + os.getcwd() + "'")

	atome.api.init()
	influxdb.api_v2.init()

	lConfJsonDict	= {
		"atome"	:	atome.config.toDict(),
		"influxdb":	influxdb.config.toDict()
	}
	log.info(
		"Config:\n%s",
		json.dumps(
			lConfJsonDict,
			indent = 4
		)
	)

	# Set timestamp of next data collection.
	# By default, this script collects all data at startup.
	lDateNextGetDataDay	= datetime.now()
	lDateNextGetDataMonth	= datetime.now()
	lDateNextGetDataYear	= datetime.now()

	lContinue	= True
	while lContinue is True:

		# lJsonData = atome_getConsumptionSinceSOD(token, user_ids, 0)
		lDateCurrent	= datetime.now()
		try:

			do_collectLive()

			if lDateNextGetDataDay <= lDateCurrent:
				lDateNextGetDataDay	= lDateCurrent + timedelta( seconds=30 )
				try:
					do_collectHistory("day")
				except:
					lDateNextGetDataDay	= lDateCurrent
					raise

			if lDateNextGetDataMonth <= lDateCurrent:
				lDateNextGetDataMonth	= lDateCurrent + timedelta( hours=1 )
				try:
					do_collectHistory("month")
				except:
					lDateNextGetDataMonth	= lDateCurrent
					raise

			if lDateNextGetDataYear <= lDateCurrent:
				lDateNextGetDataYear	= lDateCurrent + timedelta( hours=1 )
				try:
					do_collectHistory("year")
				except:
					lDateNextGetDataYear	= lDateCurrent
					raise

		except atome.exceptions.AtomeException as ex:
			log.info("Atome exception: " + str(ex) )
			continue

		except atome.exceptions.CollectException as ex:
			log.info("Collection exception: " + str(ex) )
			continue

		except atome.exceptions.LoginException as ex:
			log.info("Login exception: " + str(ex) )
			continue

		except Exception as exc:
			log.error(exc)
			# raise
			# sys.exit(1)
			continue

		else:
			log.debug("Wait for next loop...")
			# time.sleep( 1 )
			pause.until(lDateCurrent + timedelta(seconds=1))

# ##############################################################################
# ##############################################################################
#
##  @brief  Entry point.
#
if __name__ == "__main__":
	main()

# ##############################################################################
# ##############################################################################
