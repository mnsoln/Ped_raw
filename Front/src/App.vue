<template> 
<div>
  <RouterLink to="/">Table  </RouterLink>

  <RouterLink to="/ping"> Ping </RouterLink>
</div>
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style>
#app {
  margin-top: 60px
}
</style>