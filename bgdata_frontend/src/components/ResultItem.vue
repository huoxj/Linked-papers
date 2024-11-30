<script setup lang="ts">

import {ref} from "vue";
import router from "@/router";
import type {PaperContent} from "@/utils/types";
import {
  reqPaperAbstract,
  reqPaperCategory,
  reqPaperContentBrief,
  reqPaperReference,
  reqPaperTitle,
  reqPaperYear
} from "@/api/paper";

const props = defineProps(['paperId'])

const paperId = ref(props.paperId);
const paper = ref<PaperContent>({title: "", year: "", category: "", abstract: "", refCount: 0});

const title = ref<string>("");
const abstract = ref<string>("");
const year = ref<string>("");
const category = ref<string>("");
const refCount = ref<number>(0);

reqPaperTitle(props.paperId).then(res => { title.value = res.data; })
reqPaperAbstract(props.paperId).then(res => { abstract.value = res.data; })
reqPaperYear(props.paperId).then(res => { year.value = res.data; })
reqPaperCategory(props.paperId).then(res => { category.value = res.data; })
reqPaperReference(props.paperId).then(res => { refCount.value = res.data.length; })

function toPaper() {
  router.push({
    path: "/paper/" + props.paperId
  })
}

</script>

<template>
  <v-card
    class="card"
    elevation="1"
    link
    @click="toPaper"
  >
    <template v-slot:title >
      <p class="h2 theme-dark" >{{paper.title}}</p>
    </template>
    <template v-slot:subtitle>
      <v-container style="padding: 0">
        <v-row no-gutters>
          <v-col md="1" class="">{{paper.year}}</v-col>
          <v-col md="1">{{paper.category}}</v-col>
          <v-col md="2">{{paper.refCount}} References</v-col>
        </v-row>
      </v-container>
    </template>
    <template v-slot:text>
        <p class="theme-gray h4">{{paper.abstract}}</p>
    </template>
  </v-card>
</template>

<style scoped>
.card {
  margin-bottom: 20px;
  width: 130vh;
  height: 20vh;
  align-self: center;
}
</style>