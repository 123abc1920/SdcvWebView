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
              class="accordion-button collapsed py-1 bg-transparent"
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
            <div class="accordion-body bg-transparent p-2">
              <div class="mb-0">
                <div class="dropdown d-inline-block">
                  <button
                    class="btn btn-outline-transparent bg-transparent dropdown-toggle btn-sm"
                    type="button"
                    @click="isDropdownOpen = !isDropdownOpen"
                    :aria-expanded="isDropdownOpen ? 'true' : 'false'"
                  >
                    Выбрать словарь
                  </button>
                  <ul
                    class="dropdown-menu overflow-y-auto"
                    :class="{ show: isDropdownOpen }"
                  >
                    <li
                      v-for="(option, index) in availableOptions"
                      :key="index"
                    >
                      <button
                        class="dropdown-item"
                        type="button"
                        @click="selectOption(option)"
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
                    class="badge bg-dark d-flex align-items-center gap-2 fs-6 px-2 py-1 rounded text-light fw-light"
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
          <hr class="border-top border-2 border-primary my-2 w-100" />
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
import Cookies from "js-cookie";

import ResultTemplate from "./result.vue";
import ErrorTemplate from "./error.vue";

const word = ref("");
const results = ref([]);

const errorTitle = ref("");
const errorDetail = ref("");

const availableOptions = ref([]);
const isDropdownOpen = ref(false);

onMounted(async () => {
  try {
    const response = await fetch("http://127.0.0.1:5200/dicts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sdcv_type: `${Cookies.get("sdcvType")}`,
        container_name: `${Cookies.get("containerName")}`,
      }),
    });
    const data = await response.json();

    if (response.status == 200) {
      availableOptions.value = data.data;
    } else {
      console.log(data.error);
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

const selectOption = (option) => {
  if (!selectedFilters.value.includes(option)) {
    selectedFilters.value.push(option);
  }
  isDropdownOpen.value = false; // Закрываем список после клика
};

const translate = async () => {
  try {
    let headersDict = { "Content-Type": "application/json" };
    const jwt = Cookies.get("jwt");

    if (jwt) {
      headersDict = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${jwt}`,
      };
    }

    const response = await fetch("http://127.0.0.1:5200/translate", {
      method: "POST",
      headers: headersDict,
      body: JSON.stringify({
        word: word.value,
        filters: selectedFilters.value,
        sdcv_type: `${Cookies.get("sdcvType")}`,
        container_name: `${Cookies.get("containerName")}`,
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
      window.dispatchEvent(new Event("add-translation"));
    }
  } catch (error) {
    errorTitle.value = "Ошибка";
    errorDetail.value = error;
  }
};
</script>

<style scoped>
.dropdown-menu {
  max-height: 200px;
}
</style>
