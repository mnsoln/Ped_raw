<template>
  <div class="d-flex justify-content-center align-items-center">
    <button type="button" class="btn btn-warning" @click="getPingPong">{{ msg }}
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
      serverURL: "http://int0663.hus-integration.fr:4280",
    };
  },
  methods: {
    getPingPong() {
      const path = this.serverURL + '/ping';
      axios.post(path, { msg: this.msg })
        .then((res) => {
          this.msg = res.data;
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
