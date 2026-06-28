<template>
  <div class="accordion bg-transparent mt-2 mb-2" :id="accordionId">
    <div class="accordion-item" v-for="(item, index) in results" :key="index">
      <h2 class="accordion-header" :id="headingId + index">
        <button
          class="accordion-button collapsed py-1 btn-sm bg-transparent"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="`#${collapseId + index}`"
          aria-expanded="false"
          :aria-controls="collapseId + index"
        >
          {{ item.dict || "Словарь" }}
        </button>
      </h2>

      <div
        :id="collapseId + index"
        class="accordion-collapse collapse"
        :aria-labelledby="headingId + index"
        :data-bs-parent="`#${accordionId}`"
      >
        <div class="accordion-body bg-transparent">
          <p class="fs-6">{{ item.definition || item }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useId } from "vue";

defineProps({
  results: {
    type: Array,
    default: () => [],
  },
});

const accordionId = `accordion-${useId()}`;
const headingId = `heading-${useId()}`;
const collapseId = `collapse-${useId()}`;
</script>
