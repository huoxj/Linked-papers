<script setup lang="ts">

import Header from "@/components/Header.vue";
import {ref} from "vue";

const email = ref("");
const username = ref("");
const password = ref("");
const repeatPassword = ref("");
const isPremium = ref(false);

const features = ref([
  { name: 'Search', guest: 'mdi-checkbox-marked', free:'mdi-checkbox-marked' , premium: 'mdi-checkbox-marked' },
  { name: 'Graph', guest: 'mdi-close', free:'mdi-checkbox-marked', premium: 'mdi-checkbox-marked' },
  { name: 'Recommend', guest: 'mdi-close', free: 'mdi-close', premium: 'mdi-checkbox-marked' }
]);

const register = () => {
  console.log("email: ", email.value);
  console.log("username: ", username.value);
  console.log("password: ", password.value);
  console.log("repeatPassword: ", repeatPassword.value);
  console.log("isPremium: ", isPremium.value);
}

const repeatPasswordRules = [
  v => v === password.value || 'Passwords must match',
];

</script>

<template>
  <Header></Header>
  <v-container fluid class="py-8 h2" style="background-color: #f1f1f1; width: 100%;">
    <v-row>
      <v-col cols="12" class="text-left">
        <h1 class="h1 theme-dark" style="margin-left: auto; padding-left: 100px;">Create a new account</h1>
      </v-col>
    </v-row>
  </v-container>
  <v-container class="py-8" style="background-color: #ffffff;">
    <v-row>
      <v-col cols="12" md="6" class="pa-4">
        <v-form>
          <v-text-field variant="outlined" label="Email Address" prepend-icon="mdi-email" name="email" type="email" v-model="email" />
          <v-text-field variant="outlined" label="User Name" prepend-icon="mdi-account" name="username" type="text" v-model="username" />
          <v-text-field variant="outlined" label="Password" prepend-icon="mdi-lock" name="password" type="password" v-model="password" />
          <v-text-field variant="outlined" label="Repeat Password" prepend-icon="mdi-lock" name="repeat-password" type="password" v-model="repeatPassword"  :rules="repeatPasswordRules"/>
        </v-form>
        <div style="text-align: center">
          <v-btn color="#C12127" @click="register">Register</v-btn>
        </div>
      </v-col>
      <v-col cols="12" md="1" class="d-flex align-center">
        <v-divider vertical ></v-divider>
      </v-col>
      <v-col cols="12" md="5" class="pa-4">
        <v-row align="center">
          <v-col cols="auto">
            <v-chip color="#C12127" left>
              <v-icon size="x-large" left>mdi-trophy</v-icon>
            </v-chip>
          </v-col>
          <v-col>
            <h2 class="h2">Linked Papers Premium</h2>
          </v-col>
        </v-row>
        <v-table>
          <template v-slot:default>
            <thead>
            <tr>
              <th class="text-left">#</th>
              <th class="text-center">Guest</th>
              <th class="text-center">Free</th>
              <th class="text-center">Premium</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="item in features" :key="item.name">
              <td>{{ item.name }}</td>
              <td class="text-center theme-red"><v-icon>{{ item.guest }}</v-icon></td>
              <td class="text-center theme-red"><v-icon>{{ item.free }}</v-icon></td>
              <td class="text-center theme-red"><v-icon>{{ item.premium }}</v-icon></td>
            </tr>
            </tbody>
          </template>
        </v-table>
        <v-checkbox color="#C12127" label="Try Premium For FREE On Register" value="true" v-model="isPremium"></v-checkbox>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>

</style>