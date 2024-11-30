<script setup lang="ts">
import {ref} from "vue";
import {reqPaperAbstract, reqPaperCategory, reqPaperReference, reqPaperTitle, reqPaperYear} from "@/api/paper";

const props = defineProps(['paperId'])

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
</script>

<template>
  <v-card
    class="card"
    elevation="0"
    link
  >
    <template v-slot:text>
      <div class="h3 theme-dark">{{title}}</div>
      <v-container style="padding: 0">
        <v-row no-gutters>
          <v-col md="3" class="theme-gray h4">{{year}}</v-col>
          <v-col md="3" class="theme-gray h4">{{category}}</v-col>
          <v-col md="6" class="theme-gray h4">{{refCount}} References</v-col>
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