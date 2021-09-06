<template>
<div class="container">
  <h1>Remote Controller</h1>
  <hr>
  <div class="d-grid gap-2">
    <button class="btn btn-primary" @click="transmit('dac', 'volup')">DAC vol-up</button>
    <button class="btn btn-primary" @click="transmit('dac', 'voldown')">DAC vol-down</button>
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

</style>
