<template>
  <header>
    <nav class="navbar bg-dark text-light">
      <div class="w-100">
        <div class="mx-auto px-3">
          <a class="navbar-brand text-light fs-2 fw-bold" href="#">App Name</a>
        </div>
      </div>
    </nav>
  </header>

  <main class="mt-4 mb-4">
    <div class="mx-auto px-3" style="max-width: 1000px">
      <textarea
        class="form-control fs-5"
        placeholder="Введите слово..."
        rows="6"
      ></textarea>
      <p class="text-dark fs-5 mt-3 p-3">Результат</p>
    </div>
  </main>

  <footer class="bg-dark text-light py-3">
    <div class="mx-auto px-3">
      <p class="fs-5 text-light text-center mb-0">2026</p>
    </div>
  </footer>
</template>

<script setup>
import { ref } from "vue";

const word = ref("");
const result = ref("");

const translate = () => {
  result.value = `Вы ввели: ${word.value}`;
};
</script>
