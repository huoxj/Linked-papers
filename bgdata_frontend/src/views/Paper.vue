<script setup lang="ts">

import Header from "@/components/Header.vue";
import {ref, watch} from "vue";
import DrawerItem from "@/components/DrawerItem.vue";
import {EmptyPaperContent, type GraphLine, type GraphNode, type PaperContent} from "@/utils/types";
import PaperGraph from "@/components/PaperGraph.vue";
import router from "@/router";
import {reqPaperInfo, reqPaperReference, reqPaperRelated, reqPaperSameCategory} from "@/api/paper";
import type {RGJsonData} from "relation-graph-vue3";

// user premium status
const isPremium = sessionStorage.getItem("isPremium") === "true";
const snackbar = ref(false);
const snackbarMessage = ref("You need to be a premium user to view the full content");

watch(
  () => isPremium,
  (newValue) => {
    if (!newValue) {
      snackbarMessage.value = "You need a premium account to view this content.";
      snackbar.value = true;
    }
  },
  { immediate: true }
);

// page status

const detailTab = ref<string>("info");

const rootPaperId = ref<number>(Number(router.currentRoute.value.params.id));
const rootReferenceIdList = ref<number[]>([]);
const rootSameCategoryIdList = ref<number[]>([]);
const rootRelatedIdList = ref<number[]>([]);

const curPaper = ref<PaperContent>(EmptyPaperContent);
const curPaperReferenceIdList = ref<number[]>([]);
const curPaperSameCategoryIdList = ref<number[]>([]);
const curPaperRelatedIdList = ref<number[]>([]);

// paper info
const paperStorage = ref<{[key: number]: PaperContent}>({});
const paperExpanded = new Set<number>();

async function updatePaperInfo(paperId: number) {
  let isRoot = paperId === rootPaperId.value;
  let newJsonData: RGJsonData = {
    nodes: [],
    lines: [],
  }
  if (paperStorage.value[paperId] === undefined) {
    await reqPaperInfo(paperId).then(res => {
      paperStorage.value[paperId] = res.data;
      if(isRoot) selectNode(paperId);
    });
    newJsonData.nodes.push({
      id: String(paperId),
      data: paperStorage.value[paperId],
      expandHolderPosition: 'bottom',
      expanded: isRoot
    });
  }
  let relatedList = await reqPaperRelated(paperId).then(res => {
    return res.data;
  });
  let reqs = [] as Promise<any>[];
  relatedList.forEach(id => {reqs.push(reqPaperInfo(id))});
  await Promise.all(reqs).then(res => {
    res.forEach(paper => {
      paperStorage.value[paper.data.id] = paper.data;
      newJsonData.nodes.push({
        id: String(paper.data.id),
        data: paper.data,
        expandHolderPosition: 'bottom',
        expanded: false
      });
      newJsonData.lines.push({
        from: String(paperId),
        to: String(paper.data.id)
      });
    });
  });
  return newJsonData;
}

// graph event
function selectNode(id: number) {
  if(paperStorage.value[id] === undefined) {
    reqPaperInfo(id).then(res => {
      curPaper.value = res.data;
    })
  } else {
    curPaper.value = paperStorage.value[id];
  }
  reqPaperReference(id).then(res => {
    curPaperReferenceIdList.value = res.data;
  });
  reqPaperRelated(id).then(res => {
    curPaperRelatedIdList.value = res.data;
  });
  reqPaperSameCategory(id).then(res => {
    curPaperSameCategoryIdList.value = res.data;
  });
}

function expandNode(id: number, callback: (res: RGJsonData) => void) {
  if (paperExpanded.has(id)) {
    return;
  }
  updatePaperInfo(id).then(res => {
    paperExpanded.add(id);
    callback(res);
  });
}

// init root paper
updatePaperInfo(rootPaperId.value);
reqPaperReference(rootPaperId.value).then(res => {
  rootReferenceIdList.value = res.data;
});
reqPaperRelated(rootPaperId.value).then(res => {
  rootRelatedIdList.value = res.data;
});
reqPaperSameCategory(rootPaperId.value).then(res => {
  rootSameCategoryIdList.value = res.data;
});

</script>

<template>
  <v-app>
    <Header></Header>
    <v-snackbar v-model="snackbar" :timeout="3000" top>
      {{ snackbarMessage }}
    </v-snackbar>
    <div :class="{'blur-overlay':!isPremium}">
      <div class="graph-wrapper">
        <PaperGraph
          :root-id="rootPaperId"
          @expand-node="expandNode"
          @select-node="selectNode"
        ></PaperGraph>
      </div>
    </div>
    <!-- Left drawer -->
    <v-navigation-drawer
        class="drawer-style"
        width="400"
        color="#f1f1f1"
    >
      <v-expansion-panels multiple variant="accordion">
        <v-expansion-panel>
          <template v-slot:title>
            <p class="h2 theme-red">References</p>
          </template>
          <template v-slot:text>
            <v-divider></v-divider>
            <DrawerItem v-for="item in rootReferenceIdList" :paper-id="item" @click="selectNode(item)"></DrawerItem>
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
        <v-tab value="info">Info</v-tab>
        <v-tab value="reference">Reference</v-tab>
        <v-tab value="related">Related</v-tab>
      </v-tabs>
      <v-tabs-window v-model="detailTab">
        <v-tabs-window-item value="info">
          <div style="padding: 15px">
            <p class="theme-dark h3">{{curPaper.title}}</p>
            <v-row>
              <v-col cols="12" md="2">
                <p class="theme-gray text-body">{{curPaper.year}}</p>
              </v-col>
              <v-col cols="12" md="2">
                <p class="theme-gray text-body">{{curPaper.category}}</p>
              </v-col>
              <v-col cols="12" md="6">
                <p class="theme-gray text-body">{{curPaper.refCount}} References</p>
              </v-col>
            </v-row>
            <p class="theme-dark text-body">{{curPaper.abstract}}</p>
          </div>
        </v-tabs-window-item>
        <v-tabs-window-item value="reference">
          <DrawerItem v-for="item in curPaperReferenceIdList" :paper-id="item" :key="item"></DrawerItem>
        </v-tabs-window-item>
        <v-tabs-window-item value="related">
          <DrawerItem v-for="item in curPaperRelatedIdList" :paper-id="item" :key="item"></DrawerItem>
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
  margin-left: 400px;
  width: calc(100vw - 900px);
  height: calc(100vh - 78px);
  padding: 0;
}

.blur-overlay {
  filter: blur(20px);
  pointer-events: none;
}

.overlay-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(255, 255, 255, 0.8);
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}
</style>