#!/usr/bin/env bash

#====FOLDER====
DATA_FOLDER="/user/ssilvari/home/code/eheart/data"
OUTPUT_FOLDER="/user/ssilvari/home/Documents/temp/eheart/output"
SCRIPTS_FOLDER="/user/ssilvari/home/code/eheart/py"
PROXY=""

# Set parameters up
CONTAINER_NAME="eheart"
USER="sssilvar"

IMG_NAME=$USER"/"${CONTAINER_NAME}
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


echo -e "\n\n[  OK  ] Stoping container"
STOP_CONT="docker stop "${CONTAINER_NAME}
eval ${STOP_CONT}

echo -e "\n\n[  OK  ] Deleting container"
DEL_CONT="docker rm "${CONTAINER_NAME}
eval ${DEL_CONT}

echo -e "\n\n[  OK  ] Deleting image"
DEL_IMG="docker rmi "${IMG_NAME}
eval ${DEL_IMG}

echo -e "\n\n[  OK  ] Creating the new image: "${IMG_NAME}
CRE_IMG="docker build -t "${IMG_NAME}" --build-arg proxy="${PROXY}" "${CURRENT_DIR}
eval ${CRE_IMG}

echo -e "\n\n[  OK  ] Running container: "${CONTAINER_NAME}
CMD="docker run --name "${CONTAINER_NAME}" --rm -ti -v "${DATA_FOLDER}":/data/ -v "${OUTPUT_FOLDER}":/output -v "${SCRIPTS_FOLDER}":/py "${IMG_NAME}
echo ${CMD}
eval ${CMD}
