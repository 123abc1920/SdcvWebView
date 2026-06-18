<template>
  <div class="d-flex flex-column min-vh-100">
    <header>
      <nav class="navbar navbar-expand bg-dark text-light">
        <div class="container-fluid">
          <a class="navbar-brand text-light fs-2 fw-bold" href="#">App Name</a>
        </div>
      </nav>
    </header>

    <main class="mt-4 mb-4 flex-grow-1">
      <div class="container" style="max-width: 1000px; width: 100%">
        <textarea
          class="form-control fs-5"
          placeholder="Введите слово..."
          rows="6"
        ></textarea>

        <p class="fs-5 mt-3 p-3 rounded">Результат</p>
      </div>
    </main>

    <footer class="bg-dark text-light py-3 mt-auto">
      <div class="container-fluid">
        <p class="fs-5 text-center mb-0">2026</p>
      </div>
    </footer>
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
