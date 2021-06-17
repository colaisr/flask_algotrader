#!/bin/bash
echo "Restarting TWS"
/root/Jts/tws start&
echo "TWS started"
sleep 60
echo "finished waiting"
xdotool type tws_user
sleep 2
xdotool key Tab
sleep 2
xdotool type tws_password
xdotool key Return
echo "Finished login to TWS"