<template>
  <header>
    <nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark">
      <div class="container-fluid">
        <a class="navbar-brand fs-2 fw-bold text-light" href="#">SDCV</a>

        <button
          class="navbar-toggler"
          type="button"
          @click="isMenuOpen = !isMenuOpen"
          aria-controls="navbarNav"
          :aria-expanded="isMenuOpen.toString()"
          aria-label="Переключатель навигации"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div
          class="collapse navbar-collapse"
          :class="{ show: isMenuOpen }"
          id="navbarNav"
        >
          <div class="navbar-nav ms-auto mt-2 mt-lg-0">
            <span class="navbar-text text-light text-center fw-semibold">
              <i class="bi bi-person-fill me-2"></i> {{ userName }}
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
              @click="auth"
            >
              <i class="bi bi-box-arrow-right me-2"></i> <span>{{ acc }}</span>
            </button>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Cookies from "js-cookie";
import * as bootstrap from "bootstrap";

const acc = ref("Log in");
const userName = ref("Your Name");
const isMenuOpen = ref(false);

const checkAuth = async () => {
  const jwt = Cookies.get("jwt");

  if (jwt) {
    try {
      const response = await fetch("http://127.0.0.1:5200/get/data", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${jwt}`,
        },
      });
      const data = await response.json();

      console.log(data);

      if (response.status === 200) {
        acc.value = "Log out";
        userName.value = data.data.user_name;
      }
    } catch (error) {
      console.error("Ошибка:", error);
    }
  }
};

onMounted(async () => {
  checkAuth();
  window.addEventListener("auth-changed", checkAuth);
});

const auth = () => {
  const jwt = Cookies.get("jwt");

  if (jwt) {
    Cookies.remove("jwt");
    acc.value = "Log in";
    userName.value = "Your Name";
  } else {
    const modal = new bootstrap.Modal(document.getElementById("loginModal"));
    modal.show();
  }
};
</script>
