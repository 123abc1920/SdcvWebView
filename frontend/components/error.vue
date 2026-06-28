<template>
  <p class="fs-2 fw-bold">{{ errorTitle }}</p>
  <p class="fs-4">{{ errorDetail }}</p>
</template>

<script setup>
defineProps({
  errorTitle: {
    type: String,
  },
  errorDetail: {
    type: String,
  },
});
</script>
