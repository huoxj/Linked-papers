<script setup lang="ts">

import {ref} from "vue";

const title = ref("Evasion Attacks against Machine Learning at Test Time")
const year = ref(2013)
const category = ref("cs.CR")
const references = ref(10)
const text = ref("In security-sensitive applications, the success of machine learning depends on a thorough vetting of their resistance to adversarial data. In one pertinent, well-motivated attack scenario, an adversary may attempt to evade a deployed system at test time by carefully manipulating attack samples. In this work, we present a simple but effective gradient-based approach that can be exploited to systemati， In this work, we present a simple but effective gradient-based approach that can be exploited to systemati")

</script>

<template>
  <v-card
    class="card"
    elevation="1"
    link
  >
    <template v-slot:title >
      <p class="h2 theme-dark" >{{title}}</p>
    </template>
    <template v-slot:subtitle>
      <v-container style="padding: 0">
        <v-row no-gutters>
          <v-col md="1" class="">{{year}}</v-col>
          <v-col md="1">{{category}}</v-col>
          <v-col md="2">{{references}} References</v-col>
        </v-row>
      </v-container>
    </template>
    <template v-slot:text>
        <p class="theme-gray h3">{{text}}</p>
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