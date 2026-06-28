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
                class="form-control"
                id="floatingInput"
                placeholder="name@example.com"
                required
                v-model="login"
              />
              <label for="floatingInput">Имя</label>
            </div>

            <div class="form-floating mb-3">
              <input
                type="password"
                class="form-control"
                id="floatingPassword"
                placeholder="Password"
                required
                v-model="password"
              />
              <label for="floatingPassword">Пароль</label>
            </div>

            <p class="fs-4 text-center text-danger">{{ errorDetail }}</p>

            <button
              type="submit"
              class="btn btn-dark w-100 py-2 mt-2 rounded"
              @click="logIn"
            >
              Войти в аккаунт
            </button>
            <button
              type="submit"
              class="btn btn-light w-100 py-2 mt-2 rounded"
              @click="signUp"
            >
              Регистрация
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { Modal } from "bootstrap";
import Cookies from 'js-cookie';

const login = ref("");
const password = ref("");
const errorDetail = ref("");

const logIn = async () => {
  try {
    const response = await fetch("http://127.0.0.1:5200/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_name: login.value,
        password: password.value,
      }),
    });
    const data = await response.json();
    errorDetail.value = "";

    if (response.status === 200) {
      document.querySelector("#loginModal .btn-close")?.click();
      let jwt = data.data;
      Cookies.set("jwt", jwt, { expires: 7 });
    } else {
      errorDetail.value = data.error;
    }
  } catch (error) {
    errorDetail.value = error;
  }
};

const signUp = async () => {
  try {
    const response = await fetch("http://127.0.0.1:5200/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_name: login.value,
        password: password.value,
      }),
    });
    const data = await response.json();
    errorDetail.value = "";

    if (response.status === 200) {
      document.querySelector("#loginModal .btn-close")?.click();
      jwt = data.data;
    } else {
      errorDetail.value = data.error;
    }
  } catch (error) {
    errorDetail.value = error;
  }
};
</script>
