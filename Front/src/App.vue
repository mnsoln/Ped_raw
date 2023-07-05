<template>
  <!-- <div class="text-center">
            <h1><a class="text-dark" href="#" style="serif;
  font-size: 4.5rem;  text-decoration: none;">Ped_raw</a></h1>
  <Button  raised button severity="help" style="font-size: 1.5rem; margin: 0.5rem"> <a href="/" class="navbar-brand"> Pedigree </a> </Button>
          <Button class="mb-2"  severity="warning" style="font-size: 1.5rem; margin: 0.5rem;">
          <a href="/doc" class="navbar-brand"> Documentation </a>
          </Button>
          </div>
           -->

  <ul class="list-unstyled">
    <div class="nav-scroller py-1 mb-2">
      <nav class="nav d-flex justify-content-between">
        <div style="display: inline-flex; float: left">
          <img src="/logoprov5.png" alt="logo">
          <h1><a class="text-dark" href="#" style="serif;
                  font-size: 4rem;  text-decoration: none; margin: 2.5rem;">
              Ped_raw</a>
          </h1>
        </div>
        <div style="display: inline-flex; float: right; margin-top: -1.5rem">
          <Button class="mb-2" severity="secondary" style="font-size: 1.9rem;  margin-top: 0.5rem;" text> <a href="/"
              class="navbar-brand"> Pedigree </a> </Button>
          <Button class="mb-2" severity="secondary" style="font-size: 1.85rem; margin: 0.5rem;" text>
            <a href="/doc" class="navbar-brand"> Documentation </a>
          </Button>
        </div>
      </nav>
      <hr style=" margin-left: 10rem; margin-top: -1.5rem; margin-bottom: 2rem;">
    </div>

  </ul>

  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&display=swap');


#app {
  margin-top: 1rem !important;
  margin-left: 0.5rem !important;
  margin-right: 0.5rem !important;
  padding: 0.5rem !important;
}

a {
  font-family: 'Playfair Display', serif;
}
</style>