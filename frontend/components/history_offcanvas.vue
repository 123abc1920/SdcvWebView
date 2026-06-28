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
      <ErrorTemplate :error-title="errorTitle" :error-detail="errorDetail" />
      <HistoryElement v-for="item in historyArr" :key="item.id" :item="item" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

import ErrorTemplate from "./error.vue";

const historyArr = ref([]);
const errorTitle = ref("");
const errorDetail = ref("");

onMounted(async () => {
  const response = await fetch("http://127.0.0.1:5200/history", {
    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
  });
  const data = await response.json();

  console.log(data);

  historyArr.value = [];
  errorTitle.value = "";
  errorDetail.value = "";

  console.log(data);

  if (response.status === 200) {
    historyArr.value = data.data;
  } else if (response.status === 422) {
    errorTitle.value = "Ошибка";
    errorDetail.value = "Необходимо завести аккаунт!";
  } else {
    errorTitle.value = "Ошибка";
    errorDetail.value = data.error;
  }
});

import HistoryElement from "./history_element.vue";
</script>
