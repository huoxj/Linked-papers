<script setup lang="ts">

import Header from "@/components/Header.vue";
import {ref, watch} from "vue";
import {reqLogin} from "@/api/user";
import router from "@/router";
import {useRoute} from "vue-router";

const email = ref("");
const password = ref("");

const route = useRoute();
const snackbar = ref(false);
const snackbarMessage = ref("");

const login = () => {
  reqLogin(email.value, password.value).then(res => {
        console.log(res);
        if (res.status === 200) {
          router.push({path: "/"});
          sessionStorage.setItem("isPremium", res.data.data.premium);
          sessionStorage.setItem("token", res.data.data.token);
          sessionStorage.setItem("username", res.data.data.username);
        }
      }
  )
}

watch(
    () => route.query.message,
    (newMessage) => {
      if (newMessage) {
        snackbarMessage.value = newMessage as string;
        snackbar.value = true;
      }
    },
    {immediate: true}
);


</script>

<template>
  <Header></Header>
  <v-snackbar v-model="snackbar" :timeout="1500">
    {{ snackbarMessage }}
  </v-snackbar>
  <v-container fill-height>
    <v-row
        justify="center"
        align="center"
        class="mx-0"
    >
      <v-col cols="12" sm="8" md="4" style="padding-top: 150px; padding-bottom: 12px;">
        <h1 class="mb-4 h1 theme-dark">Log in</h1>
        <div class="theme-red" style="margin-bottom: 20px;">
          <router-link class="theme-red" to="/register">Need Registration?</router-link>
        </div>
        <v-form>
          <v-text-field
              variant="solo"
              label="Email Address"
              name="email"
              prepend-icon="mdi-email"
              type="email"
              v-model="email"
          ></v-text-field>
          <v-text-field
              variant="solo"
              label="Password"
              name="password"
              prepend-icon="mdi-lock"
              type="password"
              v-model="password"
          ></v-text-field>
        </v-form>
        <div style="text-align: center">
          <v-btn color="#C12127" @click="login" class="theme-red" size="large">Login</v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>

</template>

<style scoped>

</style>