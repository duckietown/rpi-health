#!/usr/bin/env python2
import json
import subprocess


def command_output(cmd):
    res = subprocess.check_output(cmd)
    lines = res.split('\n')
    res = {}
    for l in lines:
        if not l:
            continue
        if '=' in l:
            i = l.index('=')

            res[l[:i]] = l[i + 1:]
    return res


def go():
    health = {}
    health['clock'] = {}
    VC = "vcgencmd"
    for src in "arm core h264 isp v3d uart pwm emmc pixel vec hdmi dpi".split():
        cmd = [VC, "measure_clock", src]
        res = command_output(cmd)
        health['clock'][src] = list(res.values())[0]

    health['volts'] = {}
    for a in "core sdram_c sdram_i sdram_p".split():
        cmd = [VC, "measure_volts", a]
        res = command_output(cmd)
        health['volts'][a] = list(res.values())[0]

    cmd = [VC, "measure_temp"]
    health.update(command_output(cmd))

    health['mem'] = {}
    for a in "arm gpu".split():
        cmd = [VC, 'get_mem', a]
        health['mem'].update(command_output(cmd))

    health.update(command_output([VC, 'get_throttled']))

    tint = int(health['throttled'], 0)
    # tbin = "{0:b}".format(tint)

    # 0: under-voltage
    # 1: arm frequency capped
    # 2: currently throttled
    # 16: under-voltage has occurred
    # 17: arm frequency capped has occurred
    # 18: throttling has occurred

    bits = {'under-voltage-now': 0,
            'freq-capped-now': 1,
            'throttling-now': 2,
            'under-voltage-occurred': 16,
            'freq-capped-occurred': 17,
            'throttling-occurred': 18}

    T = health['throttled_humans'] = {}
    for k, n in bits.items():
        a = tint & (1 << n)
        T[k] = a > 0

    error = False
    warning = False
    msgs = []

    if T['throttling-now']:
        msgs.append('Error: PI is throttled')
        error = True
    if T['freq-capped-now']:
        msgs.append('Error: Frequency is capped')
        error = True
    if T['under-voltage-now']:
        msgs.append('Error: Under-voltage')
        error = True
    if T['throttling-occurred']:
        msgs.append('Warning: PI throttling occurred in the past.')
        warning = True
    if T['freq-capped-occurred']:
        msgs.append('Warning: Frequency is capped occurred in the past.')
        warning = True
    if T['under-voltage-occurred']:
        msgs.append('Warning: Under-voltage occurred in the past.')
        warning = True

    health['status'] = 'error' if error else 'warning' if warning else "ok"
    health['status_msgs'] = msgs

    return health


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        health = go()
        res = json.dumps(health, indent=4)
        self.wfile.write(res)

    def do_HEAD(self):
        self._set_headers()


import sys


def run(server_class=HTTPServer, handler_class=S, port=80):
    health = go()
    res = json.dumps(health, indent=4)
    print(res)
    print('')
    sys.stdout.flush()
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    sys.stderr.write('\n\nListening on port %s...' % port)
    httpd.serve_forever()


if __name__ == '__main__':
    run(port=8085)
