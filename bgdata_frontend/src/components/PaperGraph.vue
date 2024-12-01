<script setup lang="ts">

import RelationGraph, {type RGJsonData, type RGNode, type RGOptions, type RGUserEvent} from "relation-graph-vue3";
import {onMounted, ref, watch} from "vue";
import type {GraphNode, GraphLine} from "@/utils/types";
import Node from "@/components/Node.vue";

const props = defineProps(["rootId"]);
const emit = defineEmits(["expandNode", "selectNode"]);

const rootPaperId = ref<number>(props.rootId);

const options: RGOptions = {
  defaultExpandHolderPosition: 'bottom',
  toolBarDirection: 'h',
  toolBarPositionH: 'center',
  toolBarPositionV: 'bottom',

  defaultNodeShape: 1,
  defaultNodeColor: '#C12127',
  defaultNodeWidth: 300,


  defaultLineShape: 1,
  disableLineClickEffect: true,

  layout: {
    layoutName: 'center',
    distance_coefficient: 1.5,
  }
}

const jsonData: RGJsonData = {
  rootId: String(rootPaperId.value),
  nodes: [],
  lines: [],
}

// Graph initialization
const graphRef = ref<RelationGraph>();

onMounted(() => {
  graphRef.value?.setJsonData(jsonData);
})

expandNode(rootPaperId.value);

// select
function selectNode(node: RGNode, e: RGUserEvent) {
  emit("selectNode", node.data?.id);
}

// expand
function expandNodeHandler(node: RGNode, e: RGUserEvent) {
  node.expanded = true;
  expandNode(Number(node.data?.id));
}
function expandNode(id: number) {
  emit("expandNode", Number(id), (res:RGJsonData) => {
    graphRef.value?.appendJsonData(res);
    graphRef.value?.getInstance().focusNodeById(String(id));
  });
}

// collapse
function collapseNode(node: RGNode, e: RGUserEvent) {
  node.expanded = false;
}

</script>

<template>
  <RelationGraph
    ref="graphRef"
    :options="options"
    :on-node-expand="expandNodeHandler"
    :on-node-click="selectNode"
    :on-node-collapse="collapseNode"
  >
    <template #node="{node}">
      <Node :paper-content="node.data"/>
    </template>
  </RelationGraph>
</template>

<style scoped>

</style>