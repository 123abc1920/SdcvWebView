<template>
  <div
    class="rounded d-flex flex-row bg-primary align-items-center p-3 border border-1 border-primary mb-2"
  >
    <p class="fs-5 text-start m-0 text-light">{{ item.word }}</p>

    <button
      type="button"
      class="btn-close btn-sm btn-close-white ms-auto"
      aria-label="Закрыть"
    ></button>
  </div>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true,
  },
});
</script>
