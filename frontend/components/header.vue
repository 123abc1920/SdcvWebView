<template>
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
            <span class="navbar-text text-light text-center fw-semibold">
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
</template>
