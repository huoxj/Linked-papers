<script setup lang="ts">

import Header from "@/components/Header.vue";
</script>

<template>
  <Header></Header>
  <div class="upper-fill">
    <v-container class="search-wrapper">
      <v-row align="end" style="height: 70%" no-gutters>
        <p class="h2">Result for ""</p>
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
</template>

<style scoped>
.upper-fill {
  background-color: #f1f1f1;
  width: 100%;
  height: 20vh;
  justify-content: center;
}
.search-wrapper {
  width: 140vh;
  height: 100%;
}
.search-button {
  background-color: #C12127;
  color: white;
}
</style>