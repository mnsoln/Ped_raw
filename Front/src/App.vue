<template> 
 <div class="text-center">
            <h1><a class="text-dark" href="#" style="font-family: 'Playfair Display', Georgia, 'Times New Roman', serif;
  font-size: 5.25rem;  text-decoration: none;">Ped_raw</a></h1>
          </div>
<ul class="list-unstyled">
  
  <Toolbar>
    <template #center>
    <!-- <button class="btn btn-outline-success btn-lg" type="button">
    <RouterLink to="/" class="navbar-brand"> Table</RouterLink></button> -->
    <Button raised text severity="warning" style="font-size: 1.5rem;">
    <RouterLink to="/doc" class="navbar-brand" > Documentation </RouterLink> </Button>
    <Button raised text severity="help" style="font-size: 1.5rem;">
    <RouterLink to="/ped" class="navbar-brand" > Pedigree </RouterLink> </Button>
    &#160
    <Button raised text severity="warning" style="font-size: 1.5rem;">
    <RouterLink to="/ping" class="navbar-brand" > Ping </RouterLink> </Button>
    
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
  padding: 0.5rem !important;
}
</style>