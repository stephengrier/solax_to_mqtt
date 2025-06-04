# SolaX to MQTT gateway

This is a gateway that proxies real-time metrics from a SolaX X1 inverter and an
MQTT server. It uses the [python-solax ](https://github.com/squishykid/solax)
python module to read real-time data from the Rest API of the inverter. It was
created to work with the SolaX X1 Hybrid G4 inverter, but could easily be
modified to work with any of the inverters supported by the python-solax module.

## Usage

```
pip3 install -r requirements.txt
```

The code expects to find its configuration in `/etc/solax_to_mqtt.yaml`. The
`solax_to_mqtt.yaml.example` file contains an example config that you can copy
and edit for your purposes:

```
cp solax_to_mqtt.yaml.example /etc/solax_to_mqtt.yaml
vim /etc/solax_to_mqtt.yaml
```

You'll probably want to run the code on a regular schedule from Cron:

```
cat /etc/crontabs/nobody
* * * * * /usr/bin/solax_to_mqtt.py
```

