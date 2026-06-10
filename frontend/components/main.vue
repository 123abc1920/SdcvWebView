<template>
  <div class="container mt-5">
    <input v-model="word" class="form-control" placeholder="Введите слово" />
    <button @click="translate" class="btn btn-primary mt-2">Перевести</button>
    <pre class="mt-3">{{ result }}</pre>
  </div>
</template>

<script setup>
import { ref } from "vue";

const word = ref("");
const result = ref("");

const translate = () => {
  result.value = `Вы ввели: ${word.value}`;
};
</script>
