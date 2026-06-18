<template>
  <div class="d-flex flex-column min-vh-100">
    <header>
      <nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark">
        <div class="container-fluid">
          <a class="navbar-brand fs-2 fw-bold text-light" href="#">SDCV</a>

          <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Переключатель навигации"
          >
            <span class="navbar-toggler-icon"></span>
          </button>

          <div class="collapse navbar-collapse" id="navbarNav">
            <div class="navbar-nav ms-auto mt-2 mt-lg-0">
              <span
                class="navbar-text text-light text-center fw-semibold"
              >
                <i class="bi bi-person-fill me-2"></i> your-name
              </span>

              <button
                class="btn d-flex align-items-center justify-content-center w-100 w-lg-auto"
                type="button"
                data-bs-toggle="offcanvas"
                data-bs-target="#offcanvasSettings"
                aria-controls="offcanvasSettings"
              >
                <i class="bi bi-gear-fill me-2"></i> <span>Настройки</span>
              </button>

              <button
                class="btn d-flex align-items-center justify-content-center w-100 w-lg-auto"
                type="button"
                data-bs-toggle="offcanvas"
                data-bs-target="#offcanvasHistory"
                aria-controls="offcanvasHistory"
              >
                <i class="bi bi-card-list me-2"></i> <span>История</span>
              </button>

              <button
                class="btn d-flex align-items-center justify-content-center w-100 w-lg-auto"
                type="button"
                data-bs-toggle="modal"
                data-bs-target="#loginModal"
              >
                <i class="bi bi-box-arrow-right me-2"></i> <span>Выход</span>
              </button>
            </div>
          </div>
        </div>
      </nav>
    </header>

    <div
      class="offcanvas offcanvas-end text-bg-light"
      tabindex="-1"
      id="offcanvasSettings"
      aria-labelledby="offcanvasSettingsLabel"
    >
      <div class="offcanvas-header border-bottom">
        <h5 class="offcanvas-title fw-bold" id="offcanvasSettingsLabel">
          <i class="bi bi-gear-fill mx-2"></i> Настройки
        </h5>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="offcanvas"
          aria-label="Закрыть"
        ></button>
      </div>

      <div class="offcanvas-body">
        <p>настройки тут</p>
      </div>
    </div>

    <div
      class="offcanvas offcanvas-end text-bg-light"
      tabindex="-1"
      id="offcanvasHistory"
      aria-labelledby="offcanvasHistoryLabel"
    >
      <div class="offcanvas-header border-bottom">
        <h5 class="offcanvas-title fw-bold" id="offcanvasHistoryLabel">
          <i class="bi bi-card-list mx-2"></i> История
        </h5>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="offcanvas"
          aria-label="Закрыть"
        ></button>
      </div>

      <div class="offcanvas-body">
        <p>история тут</p>
      </div>
    </div>

    <main class="mt-4 mb-4 flex-grow-1 px-2">
      <div class="container-lg">
        <textarea
          class="form-control fs-5 rounded"
          placeholder="Введите слово..."
          style="resize: none; field-sizing: content; max-height: 20vh"
        ></textarea>

        <div class="accordion bg-transparent mt-2 mb-2" id="accordionSettings">
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingOne">
              <button
                class="accordion-button collapsed py-1 btn-sm"
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
              </div>
            </div>
          </div>
        </div>

        <div class="d-flex justify-content-center">
          <button type="button" class="btn btn-sm btn-dark rounded">
            <i class="bi bi-search me-2"></i> <span>Найти</span>
          </button>
        </div>

        <p class="fs-5 mt-3 p-3 rounded">Результат</p>
      </div>
    </main>

    <footer class="bg-dark text-light py-2 mt-auto">
      <div class="container-fluid">
        <p class="fs-6 text-center mb-0">2026</p>
      </div>
    </footer>

    <div
      class="modal fade"
      id="loginModal"
      tabindex="-1"
      aria-labelledby="loginModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded">
          <div class="modal-header border-bottom-0">
            <h5 class="modal-title fw-bold" id="loginModalLabel">
              <i class="bi bi-person-circle me-2"></i> Личный кабинет
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Закрыть"
            ></button>
          </div>

          <div class="modal-body py-4">
            <form @submit.prevent="handleLogin">
              <div class="form-floating mb-3">
                <input
                  type="email"
                  class="form-control"
                  id="floatingInput"
                  placeholder="name@example.com"
                  required
                />
                <label for="floatingInput">Email адрес</label>
              </div>

              <div class="form-floating mb-3">
                <input
                  type="password"
                  class="form-control"
                  id="floatingPassword"
                  placeholder="Password"
                  required
                />
                <label for="floatingPassword">Пароль</label>
              </div>

              <button
                type="submit"
                class="btn btn-dark w-100 py-2 mt-2 rounded"
              >
                Войти в аккаунт
              </button>
              <button
                type="submit"
                class="btn btn-light w-100 py-2 mt-2 rounded"
              >
                Регистрация
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
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
