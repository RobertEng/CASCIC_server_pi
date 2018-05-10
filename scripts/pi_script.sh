#!/bin/bash
# go to cascic directory
cd ~/cascic

# take an image
raspistill -o images/$OUTPUT_FILENAME

# run relevant CV package on image
python opencv_ped.py -i images/

# POST images to website
echo "sending images to site: "
curl -XPOST -F "file=@/home/pi/cascic/images/${OUTPUT_FILENAME}" "hed-kount-stage.herokuapp.com/uploader?cam_key=${CAM_KEY}"
curl -XPOST -F "file=@/home/pi/cascic/images/pred_${OUTPUT_FILENAME}" "hed-kount-stage.herokuapp.com/uploader?cam_key=${CAM_KEY}"