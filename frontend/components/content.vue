<template>
  <main class="mt-4 mb-4 flex-grow-1 px-2">
    <div class="container-lg">
      <textarea
        class="form-control fs-5 rounded"
        placeholder="Введите слово..."
        style="resize: none; field-sizing: content; max-height: 20vh"
        v-model="word"
      ></textarea>

      <div class="accordion bg-transparent mt-2 mb-2" id="accordionSettings">
        <div class="accordion-item">
          <h2 class="accordion-header" id="headingOne">
            <button
              class="accordion-button collapsed py-1 btn-sm bg-transparent"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#collapseOne"
              aria-expanded="false"
              aria-controls="collapseOne"
            >
              Настройки
            </button>
          </h2>

          <div
            id="collapseOne"
            class="accordion-collapse collapse"
            aria-labelledby="headingOne"
            data-bs-parent="#accordionSettings"
          >
            <div class="accordion-body bg-transparent">
              <div class="mb-0">
                <div class="dropdown d-inline-block me-2 mb-2">
                  <button
                    class="btn btn-outline-secondary dropdown-toggle btn-sm"
                    type="button"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                  >
                    Выбрать словарь
                  </button>
                  <ul class="dropdown-menu overflow-y-auto">
                    <li
                      v-for="(option, index) in availableOptions"
                      :key="index"
                    >
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

                <div
                  class="d-inline-flex flex-wrap gap-2 align-items-center px-1 py-2"
                >
                  <span
                    v-for="filter in selectedFilters"
                    :key="filter"
                    class="badge bg-dark d-flex align-items-center gap-2 fs-6 px-1 rounded text-light fw-light"
                  >
                    {{ filter }}
                    <button
                      type="button"
                      class="btn-close btn-close-white"
                      style="font-size: 0.6rem"
                      aria-label="Удалить"
                      @click="removeFilter(filter)"
                    ></button>
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="d-flex justify-content-center">
        <button
          type="button"
          class="btn btn-sm btn-dark rounded"
          @click="translate"
        >
          <i class="bi bi-search me-2"></i> <span>Найти</span>
        </button>
      </div>

      <div class="mt-3">
        <ResultTemplate :results="results" />
        <ErrorTemplate :error-title="errorTitle" :error-detail="errorDetail" />
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from "vue";

import ResultTemplate from "./result.vue";
import ErrorTemplate from "./error.vue";

const word = ref("");
const results = ref([]);

const errorTitle = ref("");
const errorDetail = ref("");

const availableOptions = ref([]);

onMounted(async () => {
  try {
    const response = await fetch("http://127.0.0.1:5200/dicts", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    const data = await response.json();

    if (data.data) {
      availableOptions.value = data.data;
    }
  } catch (error) {
    console.error("Ошибка загрузки словарей:", error);
  }
});

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

const translate = async () => {
  try {
    const response = await fetch("http://127.0.0.1:5200/translate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        word: word.value,
        filters: selectedFilters.value,
      }),
    });
    const data = await response.json();
    errorTitle.value = "";
    errorDetail.value = "";
    results.value = [];

    if (data.error) {
      errorTitle.value = "Ошибка";
      errorDetail.value = data.error;
    } else {
      results.value = data.data;
    }
  } catch (error) {
    errorTitle.value = "Ошибка";
    errorDetail.value = "Сервер недоступен";
  }
};
</script>

<style scoped>
.dropdown-menu {
  max-height: 200px;
}
</style>
