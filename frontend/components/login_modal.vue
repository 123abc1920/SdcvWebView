<template>
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

            <button type="submit" class="btn btn-dark w-100 py-2 mt-2 rounded">
              Войти в аккаунт
            </button>
            <button type="submit" class="btn btn-light w-100 py-2 mt-2 rounded">
              Регистрация
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
