#!/bin/bash
# make sure we aren't running more than one instance of this program
LOCKFILE=/tmp/lock.txt

if [ -e ${LOCKFILE} ] && kill -0 'cat ${LOCKFILE}'; then
  echo "already running"
  exit
fi

trap "rm -f ${LOCKFILE}; exit" INT TERM EXIT
echo $$ > ${LOCKFILE}

# go to cascic directory
cd ~/CASCIC_server_pi/algorithms

# remove images if they exist
rm -f images/$OUTPUT_FILENAME images/pred_$OUTPUT_FILENAME

# take an image
raspistill -n -o images/$OUTPUT_FILENAME

# POST images to website
echo "sending images to site: "
curl -XPOST -F "file=@/home/pi/CASCIC_server_pi/algorithms/images/${OUTPUT_FILENAME}" "hed-kount-stage.herokuapp.com/uploader?cam_key=${CAM_KEY}"

rm -f ${LOCKFILE}
