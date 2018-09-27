# RPI Health check 

## Run as container

Run as follows:
    
    $ docker run --privileged --network=host -d duckietown/rpi-health


## Run it manually

Quickly run over ssh as follows:

	$ ssh duckiebot.local python < health.py

The program reports the output in JSON on stdout.

Then it starts listening on port 8085. 
You can get the output as JSON over http as follows:

	$ wget http://duckiebot.local:8085


## Output interpretation

The output is a JSON structure as follows:

```
{
    "status": "error",
    "status_msgs": [
        "Error: PI is throttled",
        "Error: Under-voltage",
        "Warning: PI throttling occurred in the past.",
        "Warning: Under-voltage occurred in the past."
    ]

    "temp": "52.6'C",
    "clock": {
        "core": "250000000",
        "hdmi": "163683000",
        "emmc": "200000000",
        "h264": "250000000",
        "isp": "250000000",
        "pixel": "25200000",
        "uart": "48000000",
        "v3d": "0",
        "vec": "0",
        "pwm": "0",
        "arm": "600064000",
        "dpi": "0"
    },
    "mem": {
        "gpu": "128M",
        "arm": "896M"
    },
    "volts": {
        "sdram_i": "1.2500V",
        "core": "1.2000V",
        "sdram_c": "1.2500V",
        "sdram_p": "1.2250V"
    },
    "throttled_humans": {
        "throttling-now": true,
        "throttling-occurred": true,
        "freq-capped-now": false,
        "freq-capped-occurred": false,
        "under-voltage-now": true,
        "under-voltage-occurred": true
    },
    "throttled": "0x50005",
}
```

Where:

- `status` is either `ok`, `error`, `warning`.
- `status_msgs` contains explanations of errors/warnings.
- `temp` is the temperature
- The rest are other detailed information provided by `vcgencmd`. 


## TODOs

TODO: Check temperature level.

TODO: Check good memory split.

TODO: Run as container.

TODO: Make the result of the health check count as Docker health check using HEALTHCHECK command.

See: https://blog.newrelic.com/engineering/docker-health-check-instruction/

