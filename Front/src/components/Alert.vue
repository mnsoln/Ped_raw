<template>
  <div>
    <Message :life="6000" severity="info" :sticky="false">{{ message }}</Message>
  </div>
</template>
  
<script>
import Message from 'primevue/message';
export default {
  props: ['message'],
};
</script>