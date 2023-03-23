mosquitto_pub -h localhost -p 21883 -m "get.id()" -t /dev/sirrosteste/UCS_AMV-11/cmd
sleep 2
mosquitto_pub -h localhost -p 21883 -m "get.id()" -t /dev/sirrosteste/UCS_AMV-15/cmd
sleep 2
mosquitto_pub -h localhost -p 21883 -m "get.id()" -t /dev/sirrosteste/UCS_AMV-17/cmd
sleep 2
mosquitto_pub -h localhost -p 21883 -m "get.config()" -t /dev/sirrosteste/UCS_AMV-11/cmd
sleep 2
mosquitto_pub -h localhost -p 21883 -m "get.config()" -t /dev/sirrosteste/UCS_AMV-15/cmd
sleep 2
mosquitto_pub -h localhost -p 21883 -m "get.config()" -t /dev/sirrosteste/UCS_AMV-17/cmd
