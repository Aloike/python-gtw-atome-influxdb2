FROM python:3.9

# ENV DEBIAN_FRONTEND=noninteractive


# ------------------------------------------------------------------------------
# Copy sources
# ------------------------------------------------------------------------------

# ENV GIT_REPO=https://github.com/Aloike/python-gtw-atome-influxdb2

ENV APPLICATION_DIR_SRC=/app/
# ENV APPLICATION_DIR_INSTALL=/usr/local/py
ENV APPLICATION_DIR_INSTALL=${APPLICATION_DIR_SRC}


# Download application sources
COPY app_snapshot/ ${APPLICATION_DIR_SRC}
WORKDIR ${APPLICATION_DIR_SRC}
# RUN \
#                 git clone ${GIT_REPO} .

# ------------------------------------------------------------------------------
# Install dependencies
# ------------------------------------------------------------------------------

# # Install system dependencies
# RUN \
#                 apt update \
#         &&      apt-get install -y \
#                         apt-transport-https \
#                         ca-certificates \
#                         curl \
#                         git \
#                         gnupg-agent \
#                         python3-distutils \
#                         software-properties-common \
#                         vim \
#         &&      rm -rf /var/lib/apt/lists/*


# # Install Pip
# RUN \
#                 cd /tmp/ \
#         &&      wget https://bootstrap.pypa.io/get-pip.py \
#         &&      python3 get-pip.py --prefix=/usr/local \
#         &&      python3 -m pip install requests \
#         &&      pip install unidecode


# Install Pip packages
RUN	pip3 install -r ${APPLICATION_DIR_SRC}/requirements.txt



# ------------------------------------------------------------------------------
# Update configuration files
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------------------------
# Note: This should ideally be run in the same command where we're doing the `apt update`.
# RUN \
#               apt remove -y \
#                       git \
#                       vim \
#       &&      apt autoremove -y \
#       &&      rm -rf /var/lib/apt/lists/*


# ------------------------------------------------------------------------------
# Execution
# ------------------------------------------------------------------------------

# Set the workdir when running the application.
ENV APPLICATION_DIR_EXEC=/mnt/gtw-atome-influxdb2/workdir

WORKDIR ${APPLICATION_DIR_EXEC}

CMD [ "python3", "/app/main.py" ]
