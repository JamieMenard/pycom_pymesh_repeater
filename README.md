# Pymesh Lora Repeater

This is mostly vanilla pymesh code with the addition of some remote commands Use with firmware 1.20.2.r1
Hardware built by stuffing a Pysense and Lopy4 into a Mr Beams Solar Powered light.

Use from REPL by cli commands 's' enter, mac address you want to get data from,
enter, then one of the following messages.

XX = mac address to send data to; 1, 2, 10, etc

JM send self XX

JM batt level XX

JM RESET

JM send baro

JM send temp

JM set time

JM how set
