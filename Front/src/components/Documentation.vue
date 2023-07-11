<template >
  <div class="m-4">
    <Panel class="m-3" header="How to use" toggleable>
      <p v-breathing-colors="sample">
        Firstly, you will <u> need to choose which database to work with</u> : you can use the drop-down list to select an
        existing one, or create a new one using the button and then select it.
        <br>
        Then, you will be able to <u>import data</u> or <u>add a new row</u> manually, as well as to <u>delete</u> or
        <u>modify</u> existing ones. <strong> Each one of these changes will need to be saved or they will be
          lost.</strong>
      </p>
      <p class="m-2">

        <u>Imported files</u> will need to have a special structure. They are <strong>required</strong> to have at least
        one column for patient identification named 'id', 'Patient ID' or 'ID'. Here are the possible column names which
        will be used in this website.
        They can have as many columns as you wish, they will simply be ignored if not in the following list :
      <ul>
        <li> <strong> "Patient ID" column :</strong> "id", "ID", "Patient ID" </li>
        <li> <strong> "Aliases" column :</strong> "alias", "Alias", "Aliases" </li>
        <li> <strong> "Mother" column :</strong> "mother", "Mother" </li>
        <li> <strong> "Father" column :</strong> "father", "Father" </li>
        <li> <strong> "Sex" column :</strong> "sex", "Sex"
          <br><strong>Values accepted :</strong> <u>Female</u> :
          "F","Female","female",2,"2". <u>Male</u> :
          "M","Male","male",1,"1"
        </li>
        <li> <strong> "Phenotype" column :</strong> "phenotype, "Phenotype".
          <br> <strong>Values accepted :</strong> <u>Affected</u> :
          "Affected","affected",2,"yes","Yes","2". <u>Unaffected</u> : "Unaffected", "unaffected","no", "No",1,"1"
        </li>
        <li> <strong> "HPO List" column :</strong> "HPOList", "hpolist", "HPO List" </li>
        <li> <strong> "Stark Tags" column :</strong> "starkTags", "Stark Tags", "starktags" </li>
      </ul>
      Moreover, you are able to <u>download</u> any of the files in CSV format.
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
  width: 96%;
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

