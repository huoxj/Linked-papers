<script setup lang="ts">

import Header from "@/components/Header.vue";
import ResultItem from "@/components/ResultItem.vue";
import {ref} from "vue";

const page = ref(1);

</script>

<template>
  <Header></Header>
  <div class="upper-fill">
    <v-container class="search-wrapper">
      <v-row align="end" style="height: 70%" no-gutters>
        <p class="h2 theme-dark">Total 0 Result(s) for ""</p>
      </v-row>
      <v-row align="end" style="height: 20%" no-gutters>
          <v-text-field
            placeholder="Search by title or abstract"
            single-line
            variant="solo"
            density="compact"
            style="width: 100%"
          >
            <template v-slot:append>
              <v-btn class="search-button" size="large" @click="toSearch">Search</v-btn>
            </template>
          </v-text-field>
      </v-row>
    </v-container>
  </div>
  <v-container>
    <v-row justify="center">
      <ResultItem v-for="id in [1, 2, 3, 4, 5]" :key="id"></ResultItem>
    </v-row>
  </v-container>
  <v-pagination :v-bind="page" length="10" total-visible="5"></v-pagination>
  <div class="bottom-fill"></div>
</template>

<style scoped>
.upper-fill {
  background-color: #f1f1f1;
  width: 100%;
  height: 25vh;
  justify-content: center;
  margin-bottom: 10px;
}
.search-wrapper {
  width: 140vh;
  height: 100%;
}
.search-button {
  background-color: #C12127;
  color: white;
}
.bottom-fill {
  height: 5vh;
}
</style>