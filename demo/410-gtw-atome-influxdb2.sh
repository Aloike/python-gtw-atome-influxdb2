#!/bin/bash

#
##  @file
##  @brief  Starts a Telegraf instance that collects metrics from the Docker
##          host.
##
##  @see    https://www.influxdata.com/influxdb-templates/influxdb-2/
##  @see    https://raw.githubusercontent.com/influxdata/community-templates/master/influxdb2_oss_metrics/influxdb2_oss_metrics.yml
#

set -e
# set -x

source bash/functions.sh
source bash/log.bash

source variables.sh
source influxdb-tokens.env


THIS_SCRIPT_RSRC_DIR="gtw-atome-influxdb2.d"

DIR_APP_SNAPSHOT="${THIS_SCRIPT_RSRC_DIR}/app_snapshot/"


#
# Prerequisites for image build
#
LOG_INFO "Setup prerequisites for image build..."
LOG_LEVEL_INC


LOG_INFO "Create a snapshot of the app..."
if [ ! -d "${DIR_APP_SNAPSHOT}" ]
then
	mkdir -v ${DIR_APP_SNAPSHOT}
fi
cp -r ../src/* "${DIR_APP_SNAPSHOT}"


# Create the persistent data directory if it doesn't exist
if [[ ! -d "${GTW_ATOME_INFLUXDB2_DIR_DATA}" ]]
then
	LOG_INFO "Create the persistent data dir"
	mkdir -p "${GTW_ATOME_INFLUXDB2_DIR_DATA}"
fi


# Create the initial configuration file if it doesn't exist
lConfigFile="${GTW_ATOME_INFLUXDB2_DIR_DATA}/.config.ini"
if [[ -f "${lConfigFile}" ]]
then
	LOG_INFO "Configuration file already exists: '${lConfigFile}'"
else
	LOG_INFO "'${lConfigFile}' is not a file."
	LOG_INFO "Create the configuration file."

	# if read -d '\n' -p "Please enter the Atome login: " lAtomeLogin ; then : ; fi
	# if read -d '\n' -p "Please enter the Atome password: " -s lAtomePassword ; then : ; fi
	lAtomeLogin=$(zenity --entry --title="Initial setup of the Atome client" --text="Please set your Atome login (usually an email address):" --width=400)
	lAtomePassword=$(zenity --entry --title="Initial setup of the Atome client" --text="Please set your Atome password (the one used for accessing your data in the app):" --width=400)

	LOG_DBG "Writing the new configuration file."
	echo "[atome]" >> "${lConfigFile}"
	echo "atome_login = ${lAtomeLogin}" >> "${lConfigFile}"
	echo "atome_password = ${lAtomePassword}" >> "${lConfigFile}"
	echo -e "\n[influxdb2]" >> "${lConfigFile}"
	echo "host = ${INFLUXDB_HOST}" >> "${lConfigFile}"
	echo "port = ${INFLUXDB_PORT}" >> "${lConfigFile}"
	echo "org = ${INFLUXDB_ORG}" >> "${lConfigFile}"
	echo "bucket = ${GTW_ATOME_INFLUXDB2_INFLUXDB_BUCKET}" >> "${lConfigFile}"
	echo "token = ${GTW_ATOME_INFLUXDB2_INFLUXDB_TOKEN}" >> "${lConfigFile}"
fi

LOG_LEVEL_DEC


#
# Update the image
#
# LOG_INFO "Pull the container image tagged '${GTW_TELEGRAF_DOCKERHOST_CONTAINER_IMAGENAME}:${GTW_TELEGRAF_DOCKERHOST_CONTAINER_IMAGEVERSION}'..."
# LOG_LEVEL_INC

# docker pull ${GTW_TELEGRAF_DOCKERHOST_CONTAINER_IMAGENAME}:${GTW_TELEGRAF_DOCKERHOST_CONTAINER_IMAGEVERSION}

# LOG_INFO "Done pulling the image."
# LOG_LEVEL_DEC
LOG_INFO "Build the container..."
LOG_LEVEL_INC
(
	docker build \
		-t	${GTW_ATOME_INFLUXDB2_CONTAINER_NAME} \
		"${THIS_SCRIPT_RSRC_DIR}/"
)

LOG_LEVEL_DEC


#
# Start the container
#
LOG_INFO "Start the container..."
LOG_LEVEL_INC

F_container_remove ${GTW_ATOME_INFLUXDB2_CONTAINER_NAME}
docker run \
	-d \
	--name=${GTW_ATOME_INFLUXDB2_CONTAINER_NAME} \
	--net=${DOCKER_NETWORK_NAME} \
	-v "${GTW_ATOME_INFLUXDB2_DIR_DATA}":/mnt/gtw-atome-influxdb2/workdir/:rw \
	${GTW_ATOME_INFLUXDB2_CONTAINER_NAME}
# 	-e BAREMETAL_HOSTNAME="${HOSTNAME}" \
# 	-e INFLUXDB_HOST=${INFLUXDB_HOST} \
# 	-e INFLUXDB_ORG=${INFLUXDB_ORG} \
# 	-e INFLUXDB_PORT=${INFLUXDB_PORT} \
# 	-e INFLUXDB_BUCKET=${GTW_TELEGRAF_DOCKERHOST_INFLUXDB_BUCKET} \
# 	-e INFLUXDB_TOKEN=${GTW_TELEGRAF_DOCKERHOST_INFLUXDB_TOKEN} \
# 	-e HOST_ETC=/hostfs/etc \
# 	-e HOST_MOUNT_PREFIX=/hostfs \
# 	-e HOST_PROC=/hostfs/proc \
# 	-e HOST_RUN=/hostfs/run \
# 	-e HOST_SYS=/hostfs/sys \
# 	-e HOST_VAR=/hostfs/var \
# 	-v /:/hostfs:ro \
# 	-v /var/run/docker.sock:/var/run/docker.sock \
# 	-v $PWD/gtw-telegraf-dockerhost.d/telegraf.conf:/etc/telegraf/telegraf.conf:ro \
# 	# -e BAREMETAL_HOSTNAME="${GTW_TELEGRAF_DOCKERHOST_CONTAINER_NAME}.docker.${HOSTNAME}" \
# 	# --publish ${GTW_TELEGRAF_MAIN_HTTPLISTENER2_SERVICE_PORT}:${GTW_TELEGRAF_MAIN_HTTPLISTENER2_SERVICE_PORT} \
# 	# --publish ${GTW_TELEGRAF_MAIN_INFLUXDB2LISTENER_SERVICE_PORT}:${GTW_TELEGRAF_MAIN_INFLUXDB2LISTENER_SERVICE_PORT} \

LOG_INFO "Container is running."
LOG_LEVEL_DEC


exit $?

