<script setup lang="ts">

import {ref} from "vue";
import type {PaperContent} from "@/utils/types";

const props = defineProps(["paperContent"])

const paperContent = ref<PaperContent>(props.paperContent);

</script>

<template>
  <v-card class="card">
    <p class="h3 title">{{ paperContent.title }}</p>
    <v-row no-gutters>
      <v-col md="3" class="theme-gray">{{ paperContent.year }}</v-col>
      <v-col md="3" class="theme-gray">{{ paperContent.category }}</v-col>
      <v-col md="6" class="theme-gray">{{ paperContent.refCount }} References</v-col>
    </v-row>
  </v-card>
</template>

<style scoped>
.card {
  width: 300px;
  height: auto;
  padding: 5px;
}
.title {
  word-break: break-word;
  word-wrap: break-word;
}
</style>