<template>
  <div class="d-flex flex-column min-vh-100">
    <header>
      <nav class="navbar navbar-expand bg-dark text-light">
        <div class="container-fluid">
          <a class="navbar-brand text-light fs-2 fw-bold" href="#">App Name</a>
        </div>
      </nav>
    </header>

    <main class="mt-4 mb-4 flex-grow-1 px-2">
      <div class="container-lg">
        <textarea
          class="form-control fs-5 rounded"
          placeholder="Введите слово..."
          style="resize: none; field-sizing: content; max-height: 20vh"
        ></textarea>

        <div class="mb-3">
          <div class="dropdown d-inline-block me-2 mb-2">
            <button
              class="btn btn-outline-secondary dropdown-toggle btn-sm"
              type="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Выбрать словарь
            </button>
            <ul class="dropdown-menu overflow-y-scroll">
              <li v-for="option in availableOptions" :key="option">
                <button
                  class="dropdown-item btn-sm"
                  type="button"
                  @click="addFilter(option)"
                >
                  {{ option }}
                </button>
              </li>
            </ul>
          </div>

          <div class="d-inline-flex flex-wrap gap-2 align-items-center">
            <span
              v-for="filter in selectedFilters"
              :key="filter"
              class="badge bg-secondary d-flex align-items-center gap-2 fs-6 px-1"
            >
              {{ filter }}
              <button
                type="button"
                class="btn-close"
                style="font-size: 0.6rem"
                aria-label="Удалить"
                @click="removeFilter(filter)"
              ></button>
            </span>
          </div>
        </div>

        <p class="fs-5 mt-3 p-3 rounded">Результат</p>
      </div>
    </main>

    <footer class="bg-dark text-light py-2 mt-auto">
      <div class="container-fluid">
        <p class="fs-6 text-center mb-0">2026</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from "vue";

const word = ref("");
const result = ref("");

const availableOptions = ref([
  "Существительное",
  "Глагол",
  "Прилагательное",
  "English",
  "Русский",
]);

const selectedFilters = ref([]);

const addFilter = (option) => {
  if (!selectedFilters.value.includes(option)) {
    selectedFilters.value.push(option);
  }
};

const removeFilter = (filterToRemove) => {
  selectedFilters.value = selectedFilters.value.filter(
    (f) => f !== filterToRemove,
  );
};

const translate = () => {
  result.value = `Вы ввели: ${word.value}. Фильтры: ${selectedFilters.value.join(", ")}`;
};
</script>

<style scoped>
.dropdown-menu {
  max-height: 200px;
}
</style>
