<script setup lang="ts">
import {ref} from "vue";
import {reqPaperInfo} from "@/api/paper";
import type {PaperContent} from "@/utils/types";

const props = defineProps(['paperId'])

const paperId = ref(props.paperId);
const paper = ref<PaperContent>({id: 0, title: "", year: "", category: "", abstract: "", refCount: 0});

reqPaperInfo(paperId.value).then(res => {
  paper.value = res.data;
});

</script>

<template>
  <v-card
      class="card"
      elevation="0"
      link
  >
    <template v-slot:text>
      <div class="h3 theme-dark">{{ title }}</div>
      <v-container style="padding: 0">
        <v-row no-gutters>
          <v-col md="3" class="theme-gray h4">{{ year }}</v-col>
          <v-col md="3" class="theme-gray h4">{{ category }}</v-col>
          <v-col md="6" class="theme-gray h4">{{ refCount }} References</v-col>
        </v-row>
      </v-container>
    </template>
  </v-card>
</template>

<style scoped>
.card {
  width: 100%;
  height: auto;
  margin-top: 2px;
}

p {
  white-space: normal;
  word-wrap: break-word;
}
</style>