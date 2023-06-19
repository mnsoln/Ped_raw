

<template>
    <div>
        <div class="card">
            <Toolbar class="mb-4">
                <template #start>
                    <Button label="Ajouter" icon="pi pi-plus" severity="success"  size="small" @click="newDialog= true" />
                    <Button 
                    label="Supprimer" 
                    icon="pi pi-trash" severity="danger" size="small" 
                    @click="deletePedsDialog = true;"
                    :disabled="!selectedPeds || !selectedPeds.length"
                    />
                </template>
                <template #center>
                    <Button label="Sauvegarder les modifications" icon="pi pi-check" severity="success" class="mr-2" />
                </template>
                <template #end>
                    <FileUpload mode="basic" size="small" accept="image/*"  :maxFileSize="1000000" label="Importer" chooseLabel="Import" class="mr-2 inline-block" />
                    <Button label="Télécharger" icon="pi pi-upload" size="small" severity="help"/>
                    
                </template>
            </Toolbar>

            <DataTable ref="dt" :value="peds" v-model:selection="selectedPeds" dataKey="id" 
                :paginator="true" :rows="10"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown" :rowsPerPageOptions="[5,10,25]"
                currentPageReportTemplate="Showing {first} to {last} of {totalRecords} peds">
                <template #header>
                    <div class="flex flex-wrap gap-2 align-items-center justify-content-between">
                        <!-- <h4 class="m-0">Manage peds</h4>
						<span class="p-input-icon-left">
                            <i class="pi pi-search" />
                            <InputText v-model="filters['global'].value" placeholder="Search..." />
                        </span> -->
                        
					</div>
                </template>

                <Column selectionMode="multiple" style="width: 2rem" :exportable="false"></Column>
                <Column field="id" header="Individu" sortable style="min-width:7rem"></Column>
                <Column field="alias" header="Aliases" sortable style="min-width:10rem"></Column>
                <Column field="pere" header="Père" sortable>
                </Column>
                <Column field="mere" header="Mère" sortable style="min-width:8rem">
                    <!-- <template #body="slotProps">
                        {{formatCurrency(slotProps.data.price)}}
                    </template> -->
                </Column>
                <Column field="sexe" header="Sexe" sortable style="min-width:4rem"></Column>
                <Column field="phenotype" header="Phénotype" sortable style="min-width:12rem">
                    <!-- <template #body="slotProps">
                        <Rating :modelValue="slotProps.data.rating" :readonly="true" :cancel="false" />
                    </template> -->
                </Column>
                <Column field="listeHPO" header="Liste HPO" sortable style="min-width:12rem">
                    <!-- <template #body="slotProps">
                        <Tag :value="slotProps.data.pere" :severity="getStatusLabel(slotProps.data.pere)" />
                    </template> -->
                </Column>
                <Column field="tagStark" header="Tags Stark" sortable style="min-width:12rem">
                    <!-- <template #body="slotProps">
                        <Tag :value="slotProps.data.pere" :severity="getStatusLabel(slotProps.data.pere)" />
                    </template> -->
                </Column>
                <!-- <Column :exportable="false" style="min-width:8rem">
                    <template #body="slotProps">
                        <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editpeds(slotProps.data)" />
                        <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeletepeds(slotProps.data)" />
                    </template> 
                </Column>-->
            </DataTable>
        </div>
    </div>
    
    <Dialog v-model:visible="newDialog" :style="{width: '450px'}" header="Formulaire d'ajout de fichier Pedigree" :modal="true" class="p-fluid">
        <div class="field">
            <label for="id">Individu</label>
            <InputText id="id" v-model.trim="ped.id" required="true" 
              
              autofocus :class="{'p-invalid': submitted && !peds.id}" />
            <small class="p-error" v-if="submitted && !ped.id">Name is required.</small>
        </div>
        <div class="field">
            <label for="alias">Alias</label>
            <InputText id="alias" v-model="ped.alias" rows="3" cols="20" />
        </div>
        <div class="field">
            <label for="pere">Père</label>
            <InputText id="pere" v-model="ped.pere" rows="3" cols="20" />
        </div>
        <div class="field">
            <label for="mere">Mère</label>
            <InputText id="mere" v-model="ped.mere" rows="3" cols="20" />
        </div>
        <div class="field">
            <label for="sexe">Sexe</label> 
            <SelectButton v-model="ped.sexe" :options="sexes" aria-labelledby="basic" rows="3" cols="20" required="true" />
            
        </div>
        <div class="field">
            <label for="phenotype">Phénotype</label>
            <SelectButton v-model="ped.phenotype" :options="phenotypes" aria-labelledby="basic" rows="3" cols="20" required="true" />
        </div>
        <div class="field">
            <label for="listeHPO">listeHPO</label>
            <Chips id="listeHPO" v-model="ped.listeHPO" rows="3" cols="20" separator=","/>
        <div class="field">
            <label for="tagStark">tagStark</label>
            <Chips id="tagStark" v-model="ped.tagStark" rows="3" cols="20" separator="!"/>
        </div>
        <div>
          <Button label="Annuler" icon="pi pi-times"  severity="danger" text @click="newDialog = false" />
          
          <Button label="Continuer" icon="pi pi-check" text @click="addPed()" />
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

  </template>
  
  <script>
  import axios from 'axios';
  import Alert from './Alert.vue'
  import { ref } from 'vue';









export default {
  data() {
    return {
      peds: ref(),
      ped: ref({}),
      newDialog : ref(false),
      deletePedsDialog: ref(false),
      visible : ref(false),
      selectedPeds : ref(),
      submitted : ref(false),
      sexes : ["M", "F", "Inconnu"],
      phenotypes : ["Atteint", "Non Atteint", "Inconnu"]
    };
  },
  methods: {
    getPeds() {
      const path = 'http://int0663.hus-integration.fr:4280/ped';
      axios.get(path)
        .then((res) => {
          this.peds = res.data.peds;
          //console.log('get');
          console.log(this.peds);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    openNew() {
      //peds.value = {};
      newDialog.value = true;
    },
    addPed() {
      console.log(this.peds);
      console.log("hello");
      console.log(this.ped);
      console.log("iamhere");
      this.peds.push(JSON.parse(JSON.stringify(this.ped))); //copie dans peds (deep copy)
      this.newDialog=false;
      this.ped={};
    },
    deleteSelectedPeds() {
      this.peds = this.peds.filter(
        (val) => !this.selectedPeds.includes(val)
      );
      this.deletePedsDialog = false;
      this.selectedPeds = null;


    }
    // addPeds(payload) {
    //     const path = 'http://int0663.hus-integration.fr:4280/ped';
    //     axios.post(path, payload)
    //       .then(() => {
    //         this.getPeds();
    //         // this.message='Ajouté !';
    //         // this.showMessage=true;
    //       })
    //       .catch((error) => {
  
    //         console.log(error);
    //         this.getPeds();
    //       });
    //   },
    },
    
  created() {
    this.getPeds();
  },
};


</script>

<style>
html{
font-size: 80% !important;
}
</style>







