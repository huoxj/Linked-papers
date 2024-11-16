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
    elevation="0"
    link
  >
    <template v-slot:text>
      <div class="h3 theme-dark">{{title}}</div>
      <v-container style="padding: 0">
        <v-row no-gutters>
          <v-col md="3" class="theme-gray h4">{{year}}</v-col>
          <v-col md="3" class="theme-gray h4">{{category}}</v-col>
          <v-col md="6" class="theme-gray h4">{{references}} References</v-col>
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