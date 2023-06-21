
<template>
    <div>
        <div class="card">
            <Toolbar class="mb-4">
                <template #start>
                    <Button label="Add" icon="pi pi-plus" severity="success"  size="small" @click="newDialog= true" />
                    <Button label="Delete" 
                    icon="pi pi-trash" severity="danger" size="small" 
                    @click="deletePedsDialog = true"
                    :disabled="!selectedPeds || !selectedPeds.length"
                    />
                </template>
                <template #center>
                    <Button label="Save your changes" icon="pi pi-check" severity="success" class="mr-2" 
                    :disabled="!unsavedChanges"
                    @click="confirmSaveDialog=true"/>
                </template>
                <template #end>
                    <FileUpload mode="basic" size="small" accept="image/*"  :maxFileSize="1000000" label="Import" chooseLabel="Import" class="mr-2 inline-block" />
                    <Button label="Download" icon="pi pi-upload" size="small" @click="exportCSV($event)" severity="help"/>
                </template>
            </Toolbar>
            
            <div>     
                  <Dropdown v-model="selectedBase" :options="bases" editable placeholder="Select a Pedigree Database" class="p-invalid w-full md:w-14rem" />
            </div>

            <DataTable ref="dt" :value="peds" v-model:selection="selectedPeds" dataKey="id" 
                :paginator="true" :rows="10"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown" :rowsPerPageOptions="[5,10,25]"
                currentPageReportTemplate="Showing {first} to {last} of {totalRecords} peds">

                <Column selectionMode="multiple" style="width: 2rem" :exportable="false"></Column>
                <Column field="id" header="Individual" sortable style="min-width:7rem">
                </Column>
                <Column field="alias" header="Aliases" sortable style="min-width:10rem"></Column>
                <Column field="pere" header="Father" sortable>
                </Column>
                <Column field="mere" header="Mother" sortable style="min-width:8rem">
                </Column>
                <Column field="sexe" header="Sex" sortable style="min-width:4rem"></Column>
                <Column field="phenotype" header="Phenotype" sortable style="min-width:12rem">
                </Column>
                <Column field="listeHPO" header="HPO List" sortable style="min-width:12rem">
                </Column>
                <Column field="tagStark" header="Stark Tags" sortable style="min-width:12rem">
                </Column>
            </DataTable>
        </div>
    </div>
    
    <Dialog v-model:visible="newDialog" :style="{width: '450px'}" header="Formulaire d'ajout de fichier Pedigree" :modal="true" class="p-fluid">
      
        <div class="field">
            <label for="id">Individual</label>
            <InputText id="id" v-model.trim="ped.id" 
              required="true" 
              autofocus 
              :class="{'p-invalid': submitted && !ped.id | submitted && this.idDuplicate == true }" />
            <small class="p-error" v-if="submitted && !ped.id | submitted && this.idDuplicate == true">A unique ID is required.</small>
        </div>
        <div class="field">
            <label for="alias">Alias</label>
            <InputText id="alias" v-model="ped.alias" rows="3" cols="20" />
        </div>
        <div class="field">
            <label for="pere">Father</label>
            <InputText id="pere" v-model="ped.pere" rows="3" cols="20" />
        </div>
        <div class="field">
            <label for="mere">Mother</label>
            <InputText id="mere" v-model="ped.mere" rows="3" cols="20" />
        </div>
        <div class="field">
            <label for="sexe">Sex</label> 
            <SelectButton v-model="ped.sexe" :options="sexes" aria-labelledby="basic" rows="3" cols="20" required="true" />
            
        </div>
        <div class="field">
            <label for="phenotype">Phenotype</label>
            <SelectButton v-model="ped.phenotype" :options="phenotypes" aria-labelledby="basic" rows="3" cols="20" required="true"/>
        </div>
        <div class="field">
            <label for="listeHPO">HPO List</label>
            <Chips id="listeHPO" v-model="ped.listeHPO" rows="3" cols="20" separator=","/>
        <div class="field">
            <label for="tagStark">Stark Tags</label>
            <Chips id="tagStark" v-model="ped.tagStark" rows="3" cols="20" separator="!"/>
        </div>
        <div>
          <Button label="Annuler" icon="pi pi-times"  severity="danger" text @click="cancelAddTemp()" />
          <Button label="Continuer" icon="pi pi-check" type='submit' text @click="addPedTemp()" />
        </div>  
		</div>
    </Dialog>

    <Dialog
      v-model:visible="deletePedsDialog"
      :style="{ width: '450px' }"
      header="Confirmation"
      :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="ped"
          >  Êtes-vous certain(e) de vouloir supprimer le(s) fichier(s) sélectionné(s) ?</span
        >
        <br><br>
        <small> Les modifications ne seront pas sauvegardées tant que vous n'appuyez pas sur le bouton "Sauvegarder les modifications".</small>
      </div>
      <template #footer>
        <Button
          label="Non"
          icon="pi pi-times"
          text
          @click="deletePedsDialog = false"
        />
        <Button
          label="Oui"
          icon="pi pi-check"
          text
          @click="deleteSelectedPeds"
        />
      </template>
    </Dialog>
    
    <Dialog
      v-model:visible="confirmSaveDialog"
      :style="{ width: '450px' }"
      header="Confirmation"
      :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span v-if="ped" id="saving"
          >  Êtes-vous certain(e) de vouloir sauvegarder toutes les modifications effectuées dans le pedigree ?</span>
      </div>
      <template #footer>
        <Button
          label="Non"
          icon="pi pi-times"
          text
          @click="confirmSaveDialog = false"
        />
        <Button
          label="Oui"
          icon="pi pi-check"
          text
          @click="savePedsDef()"
        />
      </template>
    </Dialog>



    
  </template>
  
  <script>
  import axios from 'axios';
  import Alert from './Alert.vue'
  import { ref } from 'vue';
  import {isEqual} from 'lodash';





export default {
  data() {
    return {
      peds: ref(),
      ped: ref({}),
      originalTable: ref(false),
      originalPed : ref({}),
      unsavedChanges : ref(false),
      newDialog : ref(false),
      deletePedsDialog: ref(false),
      confirmSaveDialog: ref(false),
      idDuplicate: ref(false),
      visible : ref(false),
      selectedPeds : ref(),
      selectedBase: ref(),
      bases : ["1","2"],
      dt:ref(),
      submitted : ref(false),
      sexes : ["M", "F", "Unknown"],
      phenotypes : ["Affected", "Unaffected", "Missing"],
      
    };
  },
  methods: {
    getPeds() {
      const path = 'http://int0663.hus-integration.fr:4280/ped';
      axios.get(path)
        .then((res) => {
          this.peds = res.data;
          console.log(this.peds);
          if (this.originalTable==true){
            this.getOriginal();
            this.originalTable=false;
      }
        })
        .catch((error) => {
          console.error(error);
        });

    },
    getOriginal() {
      //console.log('origin debut');
      this.originalPed = JSON.parse(JSON.stringify(this.peds));
      console.log(this.originalPed);
      console.log('origin fin');
    },
    savePedsDef() {
        const path = 'http://int0663.hus-integration.fr:4280/ped';
        this.payload = JSON.parse(JSON.stringify(this.peds));
        console.log(this.peds);
        console.log("payload");
        console.log(this.payload);
        axios.post(path, this.payload)
          .then(() => {
            originalTable==true;
            this.getPeds();
            console.log('Ajouté !');
            this.confirmSaveDialog=false;
          })
          .catch((error) => {
            console.log(error);
            this.confirmSaveDialog=false;
          });
      },
      cancelAddTemp() {
        this.newDialog = false;
        this.ped={};
        this.submitted = false;
      },
    addPedTemp() {
      this.submitted=true;
      console.log("ped id",this.ped.id);
      //console.log("peds id",this.peds.value.id);
      const listeID = [];
      for (var i of this.peds){
        listeID.push(i.id)
      }
      this.idDuplicate=listeID.includes(this.ped.id);
        
      if (this.ped.id && this.idDuplicate == false){
        console.log(this.ped);
        console.log("ped à rajouter");
        this.peds.push(JSON.parse(JSON.stringify(this.ped))); //copie dans peds (deep copy)
        this.newDialog=false;
        this.ped={};
        console.log("peds apres rajout");
        console.log(this.peds);
        this.tablesChanged();
        this.submitted=false;
      }
        
      
      
      
    },
    deleteSelectedPeds() {
      this.peds = this.peds.filter(
        (val) => !this.selectedPeds.includes(val)
      );
      this.deletePedsDialog = false;
      this.selectedPeds = null;
      console.log('delete')
      console.log(this.peds);
      this.tablesChanged();

    },
    exportCSV() {
  //this.dt.value.exportCSV();
},
tablesChanged() {
  if (isEqual(this.peds, this.originalPed) ==false){
    this.unsavedChanges = true;
  } else {
    this.unsavedChanges = false;
  }
},
    },
    
  created() {
    this.originalTable = true;
    this.getPeds();
    this.unsavedChanges = false;
    console.log(this.unsavedChanges)
  },
  beforeRouteLeave (to, from , next) {
  
  if (this.unsavedChanges == false) {
    next(false)
  } else {
    const answer = window.confirm('Do you really want to leave? you have unsaved changes!');
    next()
  }
  window.onbeforeunload() 
  this.unsavedChanges ? true : null;
},
// beforeRouteUpdate (to, from , next) {
//   const answer = window.confirm('Do you really want to leave? you have unsaved changes!')
//   if (answer) {
//     next(false)
//   } else {
//     next(false)
//   }
// },

};


</script>

<style>
html{
font-size: 80% !important;
}
</style>







