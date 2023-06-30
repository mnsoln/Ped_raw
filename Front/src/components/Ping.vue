<template>
  <div class="d-flex justify-content-center align-items-center" >
    <button type="button"
     class="btn btn-warning"
     @click="getPingPong">{{ msg }}
      </button>
  </div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';
export default {
  name: 'Ping',
  data() {
    return {
      msg: ref('ping!'),
    };
  },
  methods: {
    getPingPong() {
        const path = 'http://int0663.hus-integration.fr:4280/ping';
        axios.post(path, {msg: this.msg})
          .then((res) => {
            this.msg = res.data;
            //console.log(this.msg);
          })
          .catch((error) => {
  
            console.error(error);
          });
      },
  
  },
  created() {
   
  },
};
</script>
