<template>
  <head>

  <a class="blog-header-logo text-dark" href="#">Large</a></head>
  <div>
    <div class="card">
      <Toolbar class="mb-4">
        <template #start>
          <span
              v-tooltip.right="{value: `<h6> Use this button when you have selected a database if you want to add a row. Don't forget to save your changes. </h6>`, escape:true,class:'custom-error'}"
            >
          <Button
            label="Add"
            icon="pi pi-plus"
            severity="success"
            @click="pedDialog= true"
            :disabled="!isBaseSelected"
          /> </span>
          <span
            v-tooltip.bottom="{value: `<h6> Select rows and use this button to delete them. Don't forget to save your changes. </h6>`, escape:true,class:'custom-error'}"
          >
            <Button
              label="Delete"
              icon="pi pi-trash"
              severity="danger"
              @click="deletePedsDialog = true"
              :disabled="!selectedPeds || !selectedPeds.length"
              
          /></span>
        </template>
        <template #center>
          <span
            v-tooltip.bottom="{value: `<h6> Use this button when you have made changes to a database to save them. </h6>`, escape:true,class: 'custom-error'}"
          >
            <Button
              label="Save your changes"
              icon="pi pi-check"
              severity="success"
              class="mr-2"
              size="large"
              :disabled="this.unsavedChanges==false"
              @click="confirmSaveDialog=true"
            />
          </span>
        </template>
        <template #end>
          <span
            v-tooltip.bottom="{value: `<h6> Use this button when you have selected a database to import data into it. </h6>`, escape:true,class: 'custom-error'}"
          >
          <FileUpload
            mode="basic"
            accept=".csv, .tsv, .json*"
            :maxFileSize="1000000"
            label="Import"
            chooseLabel="Import"
            class="mr-2 inline-block"
            :disabled="!isBaseSelected"
            :auto="true"
            url="http://int0663.hus-integration.fr:4280/upload"
            @upload="onUpload"

          />
          </span>
          <span
            v-tooltip.left="{value: `<h6> Use this button when you have selected a database to download its data. </h6>`, escape:true,class: 'custom-error'}"
          >
          <download-csv
            :data= "peds">
          <Button
            label="Download"
            icon="pi pi-upload"
            :disabled="!peds"
            severity="help"
          />
        </download-csv>
        </span>
        </template>
      </Toolbar>
      <Card>
        <template #content>
          <Dropdown
            v-model="selectedBase"
            :options="bases"
            editable
            placeholder="Search for or select an existing pedigree database"
            class="w-full md:w-14rem"
            style="min-width: 35rem"
            @change="selectBase()"
            
          />
          &zwnj; &zwnj; &zwnj; &zwnj; &zwnj;
          <Button
            label="Create new database"
            icon="pi pi-plus"
            severity="success"
            size="small"
            @click="createDB()"
          />
        </template>
      </Card>
      <DataTable
        ref="dt"
        :value="peds"
        v-model:editingRows="editingRows"
        v-model:selection="selectedPeds"
        v-model:filters="filters"
        dataKey="id"
        editMode="row"
        filterDisplay="row"
        @row-edit-save="onRowEditSave"
        tableClass="editable-cells-table"
        :paginator="true"
        :rows="10"
        showGridlines
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLinkLastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5,10,25]"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} peds"
      >
        <Column
          selectionMode="multiple"
          style="width: 2rem"
          :exportable="false"
        ></Column>
        <Column field="id" header="Patient ID" sortable style="min-width: 7rem">
          <template #filter="{ filterModel, filterCallback }">
            <InputText
              v-model="filterModel.value"
              v-tooltip.top.focus="'Hit any key to filter'"
              type="text"
              @keydown="filterCallback()"
              class="p-column-filter"
              placeholder="Search for an ID"
              style="width: 10rem;"
            />
          </template>
          <template #editor="{ data, field }">
            <InputText
              v-model="data[field]"
              required="true"
              style="width: 9rem"
            />
          </template>
        </Column>
        <Column field="alias" header="Aliases" sortable style="min-width: 7rem">
          <template #editor="{ data, field }">
            <InputText v-model="data[field]" style="width: 6rem" />
          </template>
        </Column>
        <Column field="father" header="Father" sortable>
          <template #editor="{ data, field }">
            <InputText v-model="data[field]" style="width: 6rem" />
          </template>
        </Column>
        <Column field="mother" header="Mother" sortable style="min-width: 8rem">
          <template #editor="{ data, field }">
            <InputText v-model="data[field]" style="width: 6rem" />
          </template>
        </Column>
        <Column field="sex" header="Sex" sortable style="min-width: 4rem">
          <template #editor="{ data, field }">
            <Dropdown
              v-model="data[field]"
              :options="sexes"
              style="width: 6rem"
              required="true"
            /> </template
        ></Column>
        <Column
          field="phenotype"
          header="Phenotype"
          style="min-width: 9rem"
          sortable
        >
          <template #editor="{ data, field }">
            <Dropdown
              v-model="data[field]"
              :options="phenotypes"
              style="width: max-content"
              required="true"
            />
          </template>
        </Column>
        <Column
          field="HPOList"
          header="HPO List"
          sortable
          style="min-width: 11rem"
        >
        <template #body="{ data, field }">
          <Chip v-for="hpo in data[field]"  severity="success"> {{ hpo }} </Chip>
        </template>
          <template #editor="{ data, field }">
            <Chips
              id="HPOList"
              v-model="data[field]"
              rows="3"
              cols="20"
              separator=","
              style="width: 6rem"
            />
          </template>
        </Column>
        <Column
          field="starkTags"
          header="Stark Tags"
          sortable
          style="min-width: 11rem"
        >
        <template #body="{ data, field }">
          <Chip v-for="starktag in data[field]" severity="success"> {{ starktag }} </Chip>
        </template>
          <template #editor="{ data, field }">
            <Chips
              id="starkTags"
              v-model="data[field]"
              rows="3"
              cols="20"
              separator="!"
              style="width: 6rem"
            />
          </template>
        </Column>
        <Column
          :rowEditor="true"
          style="width: 10%; min-width: 8rem"
          bodyStyle="text-align:center"
        ></Column>
      </DataTable>
    </div>
  </div>

  <Dialog
    v-model:visible="pedDialog"
    :style="{width: '450px'}"
    header="Pedigree file form"
    :modal="true"
    class="p-fluid"
  >
    <div class="field">
      <label for="id">Patient ID</label>
      <InputText
        id="id"
        v-model.trim="ped.id"
        required="true"
        autofocus
        :class="{'p-invalid': submitted && !ped.id | submitted && this.idDuplicate == true }"
      />
      <small
        class="p-error"
        v-if="submitted && !ped.id | submitted && this.idDuplicate == true"
        >A unique ID is required.</small
      >
    </div>
    <div class="field">
      <label for="alias">Alias</label>
      <InputText id="alias" v-model="ped.alias" rows="3" cols="20" />
    </div>
    <div class="field">
      <label for="father">Father</label>
      <InputText id="father" v-model="ped.father" rows="3" cols="20" />
    </div>
    <div class="field">
      <label for="mother">Mother</label>
      <InputText id="mother" v-model="ped.mother" rows="3" cols="20" />
    </div>
    <div class="field">
      <label for="sex">Sex</label>
      <SelectButton
        v-model="ped.sex"
        :options="sexes"
        aria-labelledby="basic"
        rows="3"
        cols="20"
        required="true"
      />
    </div>
    <div class="field">
      <label for="phenotype">Phenotype</label>
      <SelectButton
        v-model="ped.phenotype"
        :options="phenotypes"
        aria-labelledby="basic"
        rows="3"
        cols="20"
        required="true"
      />
    </div>
    <div class="field">
      <label for="HPOList">HPO List (tags separated by a comma ",")</label>
      <Chips
        id="HPOList"
        v-model="ped.HPOList"
        rows="3"
        cols="20"
        separator=","
      />
      <div class="field">
        <label for="starkTags"
          >Stark Tags (tags separated by an exclamation point "!" )</label
        >
        <Chips
          id="starkTags"
          v-model="ped.starkTags"
          rows="3"
          cols="20"
          separator="!"
        />
      </div>
      <div>
        <Button
          label="Annuler"
          icon="pi pi-times"
          severity="danger"
          text
          @click="cancelAddTemp()"
        />
        <Button
          label="Continuer"
          icon="pi pi-check"
          type="submit"
          text
          @click="addPedTemp()"
        />
      </div>
    </div>
  </Dialog>

  <Dialog
    v-model:visible="deletePedsDialog"
    :style="{ width: '450px' }"
    header="Confirmation"
    :modal="true"
  >
    <div class="confirmation-content">
      <InlineMessage severity="warn" v-if="ped" style="font-size: 10rem;">
        Are you sure you want to delete the selected file(s)?
      </InlineMessage>
      <br /><br />
      <small>
        Your changes will not be saved until you press the "Save your changes"
        button.</small
      >
    </div>
    <template #footer>
      <Button
        label="Non"
        icon="pi pi-times"
        text
        @click="deletePedsDialog = false"
      />
      <Button label="Oui" icon="pi pi-check" text @click="deleteSelectedPeds" />
    </template>
  </Dialog>

  <Dialog
    v-model:visible="confirmSaveDialog"
    :style="{ width: '450px' }"
    header="Confirmation"
    :modal="true"
  >
    <div class="confirmation-content">
      <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
      <span v-if="ped" id="saving">
        Are you sure you want to save all pedigree modifications in the {{ selectedBase }} file ?</span
      >
    </div>
    <template #footer>
      <Button
        label="No"
        icon="pi pi-times"
        text
        @click="confirmSaveDialog = false"
      />
      <Button label="Yes" icon="pi pi-check" text @click="savePedsDef()" />
    </template>
  </Dialog>

  <Dialog
    v-model:visible="duplicateDialog"
    :style="{ width: '450px' }"
    header="Error"
    :modal="true"
  >
    <div class="confirmation-content">
      <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
      <span v-if="ped" id="saving">
        The ID is already used. Every row needs to have a unique ID, please try
        again.
      </span>
    </div>
    <template #footer>
      <Button
        label="Ok"
        icon="pi pi-times"
        text
        @click="duplicateDialog = false"
      />
    </template>
  </Dialog>

  <Dialog
    v-model:visible="baseDialog"
    :style="{width: '450px'}"
    header="New database form"
    :modal="true"
    class="p-fluid"
  >
    <InlineMessage severity="warn">You will need to refresh the page to access your new database.</InlineMessage>
    <div class="field">
      <label for="name">Database Name</label>
      <InputText
        v-model="selectedBase"
        required="true"
        autofocus
        :class="{'p-invalid': submitted && !ped.id | submitted && this.idDuplicate == true }"
      />
      <small
        class="p-error"
        v-if="submitted && !ped.id | submitted && this.idDuplicate == true"
        >A unique database name is required.</small
      >
    </div>
    <template #footer>
      <Button
        label="Cancel"
        icon="pi pi-times"
        text
        @click="baseDialog = false"
      />
      <Button
        label="Confirm"
        icon="pi pi-check"
        text
        @click="chooseBase()"
      />
    </template>
  </Dialog>

  
  <Dialog
    v-model:visible="dialogUnsaved"
    :style="{width: '450px'}"
    header="New database form"
    :modal="true"
    class="p-fluid"
  >
    <InlineMessage severity="warn"> You are leaving your database with unsaved changes. Are you sure you want to cancel your changes ? </InlineMessage>

    <Button
        label="Go back"
        icon="pi pi-times"
        text
        @click="cancelChoose()"
      />
      <Button
        label="Leave this base"
        icon="pi pi-check"
        text
        @click="chooseBase()"
      />

  </Dialog>

  <Toast position ="top-right" 
  v-model:visible="unsavedChanges" severity="warn"
  summary="You have unsaved changes" />



</template>

<script>
  import axios from 'axios';
  import Alert from './Alert.vue'
  import { ref } from 'vue';
  import {isEqual} from 'lodash';
  import { FilterMatchMode } from "primevue/api";




export default {
  data() {
    return {
      peds : ref(),
      ped : ref({'id': "", 'alias': "", "father":"", "mother":"", "sex":"Unknown", "phenotype":"Missing","HPOList":[], "starkTags":[] }),
      originalTable: ref(false),
      originalPed : ref({}),
      unsavedChanges : ref(false),
      pedDialog : ref(false),
      deletePedsDialog: ref(false),
      confirmSaveDialog: ref(false),
      duplicateDialog : ref(false),
      baseDialog : ref(false),
      dialogUnsaved : ref(false),
      confirmChange : ref(false),
      idDuplicate: ref(false),
      visible : ref(false),
      isBaseSelected : ref(false),
      unsavedChanges : ref(false),
      editingRows: [],
      selectedPeds : ref(),
      selectedBase: ref(),
      bases : ref([]),
      newData : ref(),
      dt : ref(),
      submitted : ref(false),
      sexes : ["M", "F", "Unknown"],
      phenotypes : ["Affected", "Unaffected", "Missing"],
      filters : ref({ 'id': {value: null, matchMode: FilterMatchMode.CONTAINS}
      }),

    };
  },
  methods: {
    onRowEditSave( event){
      this.submitted=true;
      console.log("i am here");
      console.log(this.ped);
      console.log("event:");
      console.log(event);
      let { newData, index } = event;
      console.log("newData:", newData);
      this.getDuplicate(newData);
      if (newData.id != this.peds[index].id && this.idDuplicate==true){ // si l'id a change et qu'il existait deja
        this.duplicateDialog = true;
      } else {
        this.peds[index] = newData;
        this.tablesChanged();
      }


    },
    getPeds() {
      const path = 'http://int0663.hus-integration.fr:4280/ped';
      console.log('getpeds')
      axios.get(path)
        .then((res) => {
          this.peds = res.data;
          console.log('peds récupéré',this.peds);
          if (this.originalTable==true){
            this.getOriginal();
            this.originalTable=false;
          }
        })
        .catch((error) => {
          console.error(error);
        });

    },
    getBases() {
      const path = 'http://int0663.hus-integration.fr:4280/files'
      axios.get(path)
      .then((res) => {
        this.bases = res.data;
        console.log("getBases:", this.bases);
      });
    },
    selectBase() {
      console.log("selectbase");
      if (this.unsavedChanges == true){
        this.dialogUnsaved = true;
        } else { 
          this.chooseBase();
        }

    },
    chooseBase() {
      console.log('choose')
      this.unsavedChanges = false;
      this.dialogUnsaved = false ;
      this.selectedPeds = [];
      this.isBaseSelected = true ;
      
      const path = 'http://int0663.hus-integration.fr:4280/files'
      axios.post(path, {"mybase": this.selectedBase})
      .then(() => {
        console.log("postBase:",this.selectedBase);
      }) 
      .catch((error) => {
          console.log(error);
        })
      .finally(() => {
        console.log("finally:", this.selectedBase)
        this.getPeds();
    });
    this.baseDialog = false;
    },

    confirmChangeBase() {
      this.confirmChange = true;
      chooseBase();
    },
    cancelChoose(){
      this.dialogUnsaved = false;
      this.selectedBase = "";

    },
    createDB(){
      this.baseDialog= true;
      this.selectedBase = null;
      
    },
    getOriginal() {
      console.log("getoriginal:", this.peds)
      this.originalPed = JSON.parse(JSON.stringify(this.peds));
      console.log('peds original',this.originalPed);
      this.unsavedChanges = false;
    },
    savePedsDef() {
      const path = 'http://int0663.hus-integration.fr:4280/ped';
      this.payload = JSON.parse(JSON.stringify(this.peds));
      console.log(this.peds);
      console.log("payload");
      console.log(this.payload);
      // for (var col of this.colonnes){
      //   let this.payload[col] = "";
      // }
      axios.post(path, this.payload)
        .then(() => {
          this.originalTable=true;
          this.getPeds();
          console.log('Ajouté !');
          this.confirmSaveDialog=false;
          this.getOriginal();
          this.unsavedChanges = false;
          console.log('changes then?',this.unsavedChanges);
        })
        .catch((error) => {
          console.log(error);
          console.log('changes error?',this.unsavedChanges);
          this.confirmSaveDialog=false;
        });
        console.log('changes?',this.unsavedChanges);
    },
    cancelAddTemp() {
      this.pedDialog = false;
      this.ped = {'id': "", 'alias': "", "father":"", "mother":"", "sex":"Unknown", "phenotype":"Missing","HPOList":[], "starkTags":[] };
      this.submitted = false;
    },
    getDuplicate (ped) {
      const listeID = [];
      for (var i of this.peds){
        listeID.push(i.id);
      }
      this.idDuplicate=listeID.includes(ped.id);
    },
    addPedTemp() {
      this.submitted=true;
      console.log("ped id",this.ped.id);
      //console.log("peds id",this.peds.value.id);
      this.getDuplicate(this.ped)

      if (this.ped.id && this.idDuplicate == false){
        console.log(this.ped);
        console.log("ped à rajouter");
        this.peds.push(JSON.parse(JSON.stringify(this.ped))); //copie dans peds (deep copy)
        this.pedDialog=false;
        this.ped = {'id': "", 'alias': "", "father":"", "mother":"", "sex":"Unknown", "phenotype":"Missing","HPOList":[], "starkTags":[] };
        console.log("peds apres rajout");
        console.log(this.peds);
        this.tablesChanged();
        this.submitted=false;
      }
    },
    editPed(ped2edit) {
      this.pedDialog = true;
      console.log('ligne',this.ped);
      console.log('ligne',ped2edit);
      console.log('ligne',this.selectedPeds);

    },
    deleteSelectedPeds() {
      this.peds = this.peds.filter(
        (val) => !this.selectedPeds.includes(val)
      );
      this.deletePedsDialog = false;
      this.selectedPeds = null;
      console.log('delete');
      console.log(this.peds);
      this.tablesChanged();

    },
    exportCSV() {
      console.log("export this peds", this.peds);
    },
    tablesChanged() {
      if (isEqual(this.peds, this.originalPed) ==false){
        this.unsavedChanges = true;
      } else {
        this.unsavedChanges = false;
      }
    },
    async onUpload(event) {
      fileUp= event.files[0];
      const imgUpload = await fetch("http://int0663.hus-integration.fr:4280/upload", {
        method: "POST",
        body: files,
      });
      if (imgUpload) {
        console.log(imgUpload);
        toast.add({
          severity: "info",
          summary: "Success",
          detail: "File Uploaded",
          life: 10000,
        });
      }
    },
    
  },
  created() {
    this.originalTable = true;
    // this.getPeds();
    this.getBases();
    this.unsavedChanges = false;
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
html {
  font-size: 70% ;
}

</style>
