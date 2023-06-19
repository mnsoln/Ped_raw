<template> 
 <p class="h1"> Ped_raw</p>
<ul class="list-unstyled">
  <Toolbar>
    <template #center>
    <button class="btn btn-outline-success btn-lg" type="button">
    <RouterLink to="/" class="navbar-brand"> Table</RouterLink></button>
    <button class="btn btn-outline-success btn-lg" type="button"> 
    <RouterLink to="/ping" class="navbar-brand"> Ping</RouterLink></button>
    <button class="btn btn-outline-success btn-lg" type="button">
    <RouterLink to="/ped" class="navbar-brand"> Pedigree</RouterLink></button>
</template>
</Toolbar>
</ul>
  <RouterView />

</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style>

#app {
  margin-top: 1rem !important;
  margin-left: 0.5rem !important;
  margin-right: 0.5rem !important;
  padding-left: 0.5rem !important;
  padding-right: 0.5rem !important;
  padding: 0.5rem !important;
  font-size: 100% !important;
}
</style>