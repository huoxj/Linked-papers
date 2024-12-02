<script setup lang="ts">

import Header from "@/components/Header.vue";
import ResultItem from "@/components/ResultItem.vue";
import {ref, watch} from "vue";
import router from "@/router";
import {reqSearch} from "@/api/service";

const routerQuery = router.currentRoute.value.query;
const searchKeywords = ref<string>(routerQuery.keywords as string);
const searchIdList = ref<number[]>([]);
const page = ref(Number(routerQuery.pageIndex as string));
const totalPage = ref(1);

let searchParams = {
  key: searchKeywords.value,
  page: page.value
}

function updateList() {
  console.log(searchParams)
  reqSearch(searchParams).then(res => {
    searchIdList.value = res.data.idList;
    totalPage.value = res.data.totalPage;
  })
}

// initial search
updateList();

// watch page change
watch(page, (newPage) => {
  router.push({
    path: "/search",
    query: {
      keywords: searchKeywords.value,
      pageIndex: newPage
    }
  })
  searchParams.page = newPage;
  updateList();
  window.scrollTo(0, 0);
  //location.reload();
});

// do a new search
const inputKeywords = ref<string>("");
function doSearch() {
  router.push({
    path: "/search",
    query: {
      keywords: inputKeywords.value,
      pageIndex: 0
    }
  });
  searchKeywords.value = inputKeywords.value;
  searchParams.key = inputKeywords.value;
  searchParams.page = 1;
  page.value = 1;
  updateList();
}

</script>

<template>
  <Header></Header>
  <div class="upper-fill">
    <v-container class="search-wrapper">
      <v-row align="end" style="height: 70%" no-gutters>
        <p class="h2 theme-dark">Results for "{{searchKeywords}}"</p>
      </v-row>
      <v-row align="end" style="height: 20%" no-gutters>
          <v-text-field
            v-model="inputKeywords"
            placeholder="Search by title or abstract"
            single-line
            variant="solo"
            density="compact"
            style="width: 100%"
          >
            <template v-slot:append>
              <v-btn class="search-button" size="large" @click="doSearch()">Search</v-btn>
            </template>
          </v-text-field>
      </v-row>
    </v-container>
  </div>
  <v-container>
    <v-row justify="center">
      <ResultItem v-for="paperId in searchIdList" :paper-id="paperId" :key="paperId"></ResultItem>
    </v-row>
  </v-container>
  <v-pagination
    v-model="page"
    :length="totalPage"
    total-visible="5"
  ></v-pagination>
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