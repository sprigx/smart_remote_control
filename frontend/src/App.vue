<template>
<div class="container">
  <h1>Remote Controller</h1>
  <hr>
  <button class="btn btn-primary" @click="dacVoldown">DAC vol-down</button>
</div>
</template>

<script>
import axios from 'axios';

const baseURL = 'http://raspi-zero:8000/'

export default {
  setup() {
    const dacVoldown = () => {
      axios.post(baseURL + "control", {
        target: "dac",
        command: "voldown"
      })
    }
    return {
        dacVoldown
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
