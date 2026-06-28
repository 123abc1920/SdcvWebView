<template>
  <p class="fs-2 fw-bold text-center">{{ errorTitle }}</p>
  <p class="fs-4 text-center">{{ errorDetail }}</p>
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
