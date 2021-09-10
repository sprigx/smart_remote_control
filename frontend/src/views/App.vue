<template>
<div class="container">
  <h1 class="mt-4">Remote Controller</h1>
  <hr>
  <h3 class="mt-3">DAC</h3>
  <hr>
  <div class="d-grid gap-2 d-md-block">
    <button class="btn btn-warning btn-inline p-4" @click="transmit('dac', 'pwr')"><i class="bi bi-power"></i>Power</button>
    <button class="btn btn-primary btn-inline p-4" @click="transmit('dac', 'volup')">Vol-up</button>
    <button class="btn btn-primary btn-inline p-4" @click="transmit('dac', 'voldown')">Vol-down</button>
    <button class="btn btn-success btn-inline p-4" @click="transmit('dac', 'coax')">Coax</button>
    <button class="btn btn-success btn-inline p-4" @click="transmit('dac', 'usb')">USB</button>
    <button class="btn btn-secondary btn-inline p-4" @click="transmit('dac', 'bt')">B/T</button>
    <button class="btn btn-secondary btn-inline p-4" @click="transmit('dac', 'mute')">Mute</button>
  </div>
  <h3 class="mt-3">Fan</h3>
  <hr>
  <div class="d-grid gap-2 d-md-block">
    <button class="btn btn-warning btn-inline p-4" @click="transmit('fan', 'pwr')">Power</button>
    <button class="btn btn-primary btn-inline p-4" @click="transmit('fan', 'vol')">Vol</button>
  </div>
  <h3 class="mt-3">Air Conditioner</h3>
  <hr>
  <div class="d-grid gap-2 d-md-block">
    <button class="btn btn-warning btn-inline p-4" @click="transmit('ac', 'pwr')">Power</button>
  </div>
</div>
</template>

<script>
import axios from 'axios';

const baseURL = 'http://raspi-zero.lan:8000/'

export default {
  setup() {
    const transmit = (target, command) => {
      axios.post(baseURL + "control", {
        target: target,
        command: command
      })
    }
    return {
        transmit
      }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.btn-inline {
  margin: 10px 20px;
}

</style>
