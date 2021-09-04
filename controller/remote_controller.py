import time
import json
import os
import re
from glob import glob
import pigpio # http://abyz.co.uk/rpi/pigpio/python.html


class RemoteController:
    PRE_MS     = 200
    POST_MS    = 15
    FREQ       = 38.0
    GAP_MS     = 100
    TOLERANCE  = 15
    POST_US    = POST_MS * 1000
    PRE_US     = PRE_MS  * 1000
    GAP_S      = GAP_MS  / 1000.0

    def __init__(self, gpio):

        self.pi = pigpio.pi() # Connect to Pi.
        self.gpio = gpio

        if not self.pi.connected:
           return 1

        target = self.build_filepath('recordings/*.json')
        print(target)
        filenames = glob(target)
        self.records = {
            re.search('^.*\/(.*).json$', filename).group(1):
            self.parse_file(filename)
            for filename in filenames
        }

        self.pi.set_mode(self.gpio, pigpio.OUTPUT) # IR TX connected to this GPIO.
        self.pi.wave_add_new()
        self.emit_time = time.time()

    def build_filepath(self, relative_path):
        return os.path.join(os.path.dirname(__file__), relative_path)

    def parse_file(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def carrier(self, micros):
        gpio = self.gpio
        wf = []
        cycle = 1000.0 / self.FREQ
        cycles = int(round(micros/cycle))
        on = int(round(cycle / 2.0))
        sofar = 0
        for c in range(cycles):
            target = int(round((c+1)*cycle))
            sofar += on
            off = target - sofar
            sofar += off
            wf.append(pigpio.pulse(1<<gpio, 0, on))
            wf.append(pigpio.pulse(0, 1<<gpio, off))
        return wf

    def cleanup(self):
        self.pi.stop()

    def transmit(self, target, command):
        print('trasmit start')
        try:
            code = self.records[target][command]
        except KeyError:
            print('no record.')
            return 'No such record.'

        # Create wave
        marks_wid = {}
        spaces_wid = {}

        wave = [0]*len(code)

        for i in range(0, len(code)):
            ci = code[i]
            if i & 1: # Space
                if ci not in spaces_wid:
                    self.pi.wave_add_generic([pigpio.pulse(0, 0, ci)])
                    spaces_wid[ci] = self.pi.wave_create()
                wave[i] = spaces_wid[ci]
            else: # Mark
                if ci not in marks_wid:
                    wf = self.carrier(ci)
                    self.pi.wave_add_generic(wf)
                    marks_wid[ci] = self.pi.wave_create()
                wave[i] = marks_wid[ci]

        delay = self.emit_time - time.time()

        if delay > 0.0:
            time.sleep(delay)
        self.pi.wave_chain(wave)

        while self.pi.wave_tx_busy():
            time.sleep(0.002)
        self.emit_time = time.time() + self.GAP_S

        for i in marks_wid:
            self.pi.wave_delete(marks_wid[i])
        marks_wid = {}

        for i in spaces_wid:
            self.pi.wave_delete(spaces_wid[i])
        spaces_wid = {}
        print('transmit end')
        return 'transmit done'

if __name__ == '__main__':
    c = RemoteController(17)
    c.transmit('dac', 'voldown')
    c.transmit('dac', 'voldown')
    c.cleanup()
