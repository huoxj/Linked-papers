<script setup lang="ts">

import Header from "@/components/Header.vue";
import RelationGraph, {type RGJsonData, type RGOptions} from "relation-graph-vue3";
import {onMounted, ref} from "vue";
import DrawerItem from "@/components/DrawerItem.vue";
import type {GraphLine, GraphNode, PaperContent} from "@/utils/types";
import router from "@/router";
import {
  reqPaperAbstract,
  reqPaperContentBrief,
  reqPaperReference,
  reqPaperRelated,
  reqPaperSameCategory,
  reqPaperTitle, reqPaperYear
} from "@/api/paper";
import {it} from "vuetify/locale";

// Graph
const jsonData:RGJsonData = {
  rootId: 'N3',
  nodes: [
    { id: 'N4', text: '十4' },
    { id: 'N5', text: '十5' },
    { id: 'N6', text: '十6' },
    { id: 'N7', text: '十7' },
    { id: 'N3', text: '十三' },
    { id: 'N9', text: '152****3393' },
  ],
  lines: [
    { from: 'N3', to: 'N9', text: '分享' },
    { from: 'N3', to: 'N4', text: '分享444' },
    { from: 'N3', to: 'N5', text: '分享555' },
    { from: 'N3', to: 'N6', text: '分享666' },
    { from: 'N3', to: 'N7', text: '分享777' }
  ],
}
const options:RGOptions = {
  defaultExpandHolderPosition: 'bottom',
  defaultLineShape: 1,
  toolBarDirection: 'h',
  toolBarPositionH: 'center',
  toolBarPositionV: 'bottom',
}

const detailTab = ref<string>("abstract");

const graphRef = ref<RelationGraph>();

onMounted(() => {
  graphRef.value?.setJsonData(jsonData);
})

// root paper info
const rootPaperId = ref<number>(2);
const rootPaper = ref<PaperContent>({ title: "",  year: "",  category: "",  abstract: "",  refCount: 0 });

reqPaperAbstract(rootPaperId.value).then(res => { rootPaper.value.abstract = res.data; });
reqPaperTitle(rootPaperId.value).then(res => { rootPaper.value.title = res.data; });
reqPaperYear(rootPaperId.value).then(res => { rootPaper.value.year = res.data; });

// root paper relations id list
const rootReferenceIdList = ref<number[]>([]);
const rootSameCategoryIdList = ref<number[]>([]);
const rootRelatedIdList = ref<number[]>([]);

reqPaperReference(rootPaperId.value).then(res => {
  rootReferenceIdList.value = res.data;
})

reqPaperSameCategory(rootPaperId.value).then(res => {
  rootSameCategoryIdList.value = res.data;
})

reqPaperRelated(rootPaperId.value).then(res => {
  rootRelatedIdList.value = res.data;
})

/*
  * GRAPH
 */

// graph data

let nodes:GraphNode[] = [];
let lines:GraphLine[] = [];



const graphData:RGJsonData = {
  rootId: rootPaperId.value.toString(),
  nodes: nodes,
  lines: lines,
}


</script>

<template>
  <v-app>
    <Header></Header>

    <div class="graph-wrapper">
      <RelationGraph ref="graphRef" :options="options">
        <template #node="{node}">
          <div style="padding-top:20px;">{{node.text}}</div>
        </template>
      </RelationGraph>
    </div>

    <!-- Left drawer -->
    <v-navigation-drawer
      class="drawer-style"
      width="400"
      color="#f1f1f1"
    >
      <v-expansion-panels multiple variant="accordion">
        <v-expansion-panel >
          <template v-slot:title>
            <p class="h2 theme-red">References</p>
          </template>
          <template v-slot:text>
            <v-divider></v-divider>
            <DrawerItem v-for="item in rootReferenceIdList" :paper-id="item"></DrawerItem>
          </template>
        </v-expansion-panel>
        <v-expansion-panel>
          <template v-slot:title>
            <p class="h2 theme-red">Field paper</p>
          </template>
          <template v-slot:text>
            <v-divider></v-divider>
            <DrawerItem v-for="item in rootSameCategoryIdList" :paper-id="item"></DrawerItem>
          </template>
        </v-expansion-panel>
        <v-expansion-panel>
          <template v-slot:title>
            <p class="h2 theme-red">Related</p>
          </template>
          <template v-slot:text>
            <v-divider></v-divider>
            <DrawerItem v-for="item in rootRelatedIdList" :paper-id="item"></DrawerItem>
          </template>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-navigation-drawer>

    <!-- Right drawer -->
    <v-navigation-drawer
      class="drawer-style"
      width="500"
      location="right"
      color="#f1f1f1"
    >
      <v-tabs v-model="detailTab" grow bg-color="#FFFFFF" slider-color="#2A333C">
        <v-tab value="abstract">Abstract</v-tab>
        <v-tab value="reference">Reference</v-tab>
        <v-tab value="related">Related</v-tab>
      </v-tabs>
      <v-tabs-window v-model="detailTab">
        <v-tabs-window-item value="abstract">
          <p class="theme-dark text-body" style="padding: 15px">{{rootPaper.abstract}}</p>
        </v-tabs-window-item>
        <v-tabs-window-item value="reference">
          <DrawerItem v-for="item in [1,2,3]"></DrawerItem>
        </v-tabs-window-item>
        <v-tabs-window-item value="related">
          <DrawerItem v-for="item in [1,2,3]"></DrawerItem>
        </v-tabs-window-item>
      </v-tabs-window>
    </v-navigation-drawer>
  </v-app>

</template>

<style scoped>
.drawer-style {
  margin-top: 70px;
  max-height: calc(100vh - 70px);
}
.graph-wrapper {
  width: 100%;
  height: calc(100vh - 78px);
  padding: 0;
}
</style>