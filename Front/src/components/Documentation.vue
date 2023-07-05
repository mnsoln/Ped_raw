<template >
  <div class="m-4">
    <Panel class="m-3" header="How to use" toggleable>
      <p class="m-2">
        Firstly, you will <u> need to choose which database to work with</u> : you can use the drop-down list to select an
        existing one, or create a new one using the button and then select it.
        <br>
        Then, you will be able to <u>import data</u> or <u>add a new row</u> manually, as well as to <u>delete</u> or
        <u>modify</u> existing ones. <strong> Each one of these changes will need to be saved or they will be
          lost.</strong>
      </p>
      <p class="m-2">

        <u>Imported files</u> will need to have a special structure. They are required to have at least one id column
        named 'id', 'Patient ID' or 'ID'. Here are the possible column names which will be used in this website.
        They can have as many columns as you wish, they will simply be ignored if not in the following list :
      <ul>
        <li> <u> "Patient ID" column :</u> "id", "ID", "Patient ID" </li>
        <li> <u> "Aliases" column :</u> "alias", "Alias", "Aliases" </li>
        <li> <u> "Mother" column :</u> "mother", "Mother" </li>
        <li> <u> "Father" column :</u> "father", "Father" </li>
        <li> <u> "Phenotype" column :</u> "phenotype, "Phenotype" </li>
        <li> <u> "HPO List" column :</u> "HPOList", "hpolist", "HPO List" </li>
        <li> <u> "Stark Tags" column :</u> "starkTags", "Stark Tags", "starktags" </li>
      </ul>
      Moreover, you are able to <u>download</u> any of the files.
      </p>
    </Panel>

    <Panel class="m-3" header="Pedigree files" toggleable>
      <p class="m-2">
        Pedigree files document the structured descriptions of the familial relationship among samples in a study.
        <br>

        The files include information such as a unique identifier, their relationships, the individual's sex and their
        affected status. Our team added a list of HPO terms and tags for our Stark machine to assimilate further
        information.
        <br>

        Pedigree files are created based on information gathered from family members, medical records, or genetic testing,
        and they play a crucial role in understanding genetic inheritance patterns and conducting genetic analyses.
      </p>
    </Panel>
  </div>

  <div class="button">
    <small>Authors : &#160 &#160</small>
    <Button severity="warning" size="small" @click="getPingPong">{{ msg }}
    </Button>

  </div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';
export default {
  name: 'Ping',
  data() {
    return {
      msg: ref('MEDINA Solène !'),
    };
  },
  methods: {
    getPingPong() {
      const path = 'http://int0663.hus-integration.fr:4280/ping';
      axios.post(path, { msg: this.msg }, { withCredentials: true })
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




<style>
.p-panel-header {
  font-size: 1.55rem;
}

.m-3 {
  width: 80%;

}

.m-2 {
  font-size: 1.2rem;
  text-indent: 3%;
}

.m-4 {
  min-width: 90%;
  width: 95%;
  max-width: 98%;
  position: relative;
  top: 10%;
  left: 10%;
}

.button {
  float: right;
  margin-bottom: 2%;
  margin-right: 2%;
  display: flex;
  align-items: center;
}

body {
  overflow-x: hidden;
}
</style>

