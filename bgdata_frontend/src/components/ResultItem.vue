<script setup lang="ts">

import {ref} from "vue";
import router from "@/router";
import type {PaperContent} from "@/utils/types";
import {reqPaperContentBrief} from "@/api/paper";

const props = defineProps(['paperId'])

const paper = ref<PaperContent>({title: "", year: "", category: "", abstract: "", refCount: 0});

reqPaperContentBrief(props.paperId).then(res => {
  paper.value.title = res[0].data.text;
  paper.value.abstract = res[1].data.text;
  paper.value.year = res[2].data.text;
  paper.value.category = res[3].data.text;
  paper.value.refCount = res[4].data.length;
})

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