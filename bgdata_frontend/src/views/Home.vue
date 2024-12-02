<script setup lang="ts">

import Header from "@/components/Header.vue";
import router from "@/router";
import ResultItem from "@/components/ResultItem.vue";
import {ref} from "vue";
import {reqRecommend} from "@/api/service";
import type {PaperContent} from "@/utils/types";
import {reqPaperContentBrief} from "@/api/paper";


const recommendIdList = ref<number[]>();

// get recommend list
// reqRecommend().then(res => {
//   recommendIdList.value = res.data;
// })

const searchKeywords = ref("");

// do a simple search
function doSearch() {
  router.push({
    path: "/search",
    query: {
      keywords: searchKeywords.value,
      pageIndex: 1
    }
  });
}

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
        <v-col md="12">
          <v-text-field
              placeholder="Search by title or abstract"
              single-line
              variant="solo"
              v-model="searchKeywords"
          >
            <template v-slot:append>
              <v-btn class="search-button" size="x-large" @click="doSearch">Search</v-btn>
            </template>
          </v-text-field>
        </v-col>
      </v-row>
    </v-container>
  </div>
  <v-container style="height: 40vh">
    <v-row align="center" style="height: 40vh">
      <v-spacer></v-spacer>
      <v-col md="3">
        <v-card
          class="mx-auto"
          prepend-icon="mdi-file-settings"
          width="18vw"
          height="100%"
        >
          <template v-slot:title>
            <span class="h2 theme-dark">References</span>
          </template>
          <v-card-text class="bg-surface-light pt-4">
            <p class="h3 theme-dark">Access with Ease</p>
            <p class="text-body theme-dark">Quickly find and access the references of any paper in the search results for seamless exploration</p>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col md="4">
        <v-card
          class="mx-auto"
          prepend-icon="mdi-text-box"
          width="18vw"
          height="100%"
        >
          <template v-slot:title>
            <span class="h2 theme-dark">Abstracts</span>
          </template>
          <v-card-text class="bg-surface-light pt-4">
            <p class="h3 theme-dark">Clear & Concise</p>
            <p class="text-body theme-dark">Instantly view titles and abstracts with just one click for a quick overview of the research</p>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col md="3">
        <v-card
          class="mx-auto"
          prepend-icon="mdi-graph"
          width="18vw"
          height="100%"
        >
          <template v-slot:title>
            <span class="h2 theme-dark">Relation Graph</span>
          </template>
          <v-card-text class="bg-surface-light pt-4">
            <p class="h3 theme-dark">Explore Connections</p>
            <p class="text-body theme-dark">Effortlessly discover related papers or explore research within the same field through an intuitive relational graph</p>
          </v-card-text>
        </v-card>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  </v-container>
  <!--  <v-container width="130vh">-->
  <!--    <v-row style="margin-bottom: 5px">-->
  <!--      <p class="h2 theme-dark">Recommend for you</p>-->
  <!--      <v-divider></v-divider>-->
  <!--    </v-row>-->
  <!--    <v-row justify="center">-->
  <!--      <ResultItem v-for="paperId in recommendIdList" :paper-id="paperId"></ResultItem>-->
  <!--    </v-row>-->
  <!--  </v-container>-->
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