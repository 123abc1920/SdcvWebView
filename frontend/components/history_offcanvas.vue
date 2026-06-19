<template>
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
      <HistoryElement />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

import HistoryElement from "./history_element.vue";
</script>
