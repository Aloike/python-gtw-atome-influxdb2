#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ##############################################################################
# ##############################################################################
#
##  @brief  Thrown if an error was encountered while retrieving energy
##          consumption data.
#
class	AtomeException(Exception):
	pass

# ##############################################################################
# ##############################################################################
#
##  @brief  Thrown if an error was encountered while collecting Atome data.
#
class	CollectException(Exception):
	pass

# ##############################################################################
# ##############################################################################
#
##  @brief  Thrown if an error was encountered while connecting to the energy
##          consumption data provider.
#
class	LoginException(Exception):
	pass

# ##############################################################################
# ##############################################################################
