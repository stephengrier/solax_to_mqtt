#!/usr/bin/env python3
import solax
import asyncio
import json
import paho.mqtt.publish as publish
import yaml
from importlib.metadata import entry_points
from pathlib import Path

INVERTERS_ENTRY_POINTS = {
   ep.name: ep.load() for ep in entry_points(group="solax.inverter")
}


def load_config():
    for f in './config.yaml', '/etc/solax_to_mqtt.yaml':
        if Path(f).is_file():
            with open(f) as fh:
                return yaml.load(fh, Loader=yaml.FullLoader)


def main():
    cfg = load_config()

    async def work():
        inverter = await solax.discover(
            cfg['inverter']['host'],
            cfg['inverter']['port'],
            cfg['inverter']['password'],
            inverters=[INVERTERS_ENTRY_POINTS.get("x1_hybrid_gen4")],
            return_when=asyncio.FIRST_COMPLETED
        )
        return await inverter.get_data()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    data = loop.run_until_complete(work())

    publish.single(
        cfg['mqtt']['topic'],
        json.dumps(data.data),
        hostname=cfg['mqtt']['host'],
        port=cfg['mqtt']['port'],
        auth={
            'username': cfg['mqtt']['username'],
            'password': cfg['mqtt']['password'],
        },
        tls={'ca_certs': cfg['mqtt']['cacerts_file']},
    )


if __name__ == '__main__':
    main()
