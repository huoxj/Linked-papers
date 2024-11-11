<script setup lang="ts">

import Header from "@/components/Header.vue";
</script>

<template>
  <Header></Header>
  <div class="upper-fill">
    <v-container class="search-wrapper">
      <v-row style="height: 15vh"></v-row>
      <v-row>
        <p class="h1 theme-dark">Explore Linked Papers</p>
      </v-row>
      <v-row>
        <v-icon icon="mdi-book-open-blank-variant" size="x-large" class="theme-dark"></v-icon>
        <p class="h2 theme-gray">&nbsp Big data powered paper search engine</p>
      </v-row>
      <v-row><br><br></v-row>
      <v-row>
        <v-col md="9" >
          <v-text-field
            placeholder="Search by title or abstract"
            single-line
            variant="solo"
          ></v-text-field>
        </v-col>
        <v-col md="2">
          <v-btn class="search-button" size="x-large">Search</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
  <div>

  </div>
</template>

<style scoped>
.upper-fill {
  background-color: #f1f1f1;
  width: 100%;
  height: 45vh;
}
.search-wrapper {
  width: 140vh;
  height: 30vh;
}
.search-button {
  background-color: #C12127;
  color: white;
}
</style>