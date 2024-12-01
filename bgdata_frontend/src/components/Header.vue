<script setup lang="ts">

import {ref} from "vue";
import router from "@/router";

const username = sessionStorage.getItem("username");
const isPremium = sessionStorage.getItem("isPremium") === "true";

const logout = () => {
  sessionStorage.setItem("username", "");
  sessionStorage.removeItem("token");
  sessionStorage.removeItem("isPremium");
  router.push({path: "/"});
  // 刷新界面
  location.reload();
}

</script>

<template>
  <div class="header_wrapper">
    <v-container fluid>
      <v-row>
        <v-col md="1"></v-col>
        <v-col md="2" class="col_center">
          <router-link to="/" class="no_link">
            <p class="h2 theme-white">Linked Papers</p>
          </router-link>
        </v-col>
        <v-spacer></v-spacer>
        <v-col v-if="!username" md="2" class="col_center" style="justify-content: right">
          <router-link to="/login">
            <p class="h4 theme-white underline">Log in</p>
          </router-link>
        </v-col>
        <v-col v-if="!username" md="2" class="col_center">
          <router-link to="/register">
            <p class="h4 theme-white underline">Register for FREE</p>
          </router-link>
        </v-col>
        <v-col v-if="username" md="1" class="col_center">
          <p style="color: #f1f1f1;font-size: x-large">{{ username }}</p>
          <v-icon v-if="isPremium" style="color: gold" size="large" left>mdi-trophy</v-icon>
        </v-col>
        <v-col v-if="username" md="1"  class="col_center">
          <v-btn variant="text"  @click="logout()" style="font-size: large;color:#FFFFFF ;background: #C12127;" text="Log out"></v-btn>
        </v-col>
        <v-col md="1"></v-col>
      </v-row>
    </v-container>
  </div>
  <div style="height: 70px"></div>
</template>

<style scoped>
.header_wrapper {
  background-color: #C12127;
  width: 100%;
  height: 70px;
  position: fixed;
  top: 0;
  z-index: 999;
}

.no_link {
  text-decoration: none;
}

.underline {
  text-decoration: underline;
}

.col_center {
  display: flex;
  align-items: center;
}
</style>