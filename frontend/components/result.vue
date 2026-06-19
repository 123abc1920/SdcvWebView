<template>
  <div class="accordion bg-transparent mt-2 mb-2" :id="accordionId">
    <div class="accordion-item">
      <h2 class="accordion-header" :id="headingId">
        <button
          class="accordion-button collapsed py-1 btn-sm bg-transparent"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="`#${collapseId}`"
          aria-expanded="false"
          :aria-controls="collapseId"
        >
          Test Словарь
        </button>
      </h2>

      <div
        :id="collapseId"
        class="accordion-collapse collapse"
        :aria-labelledby="headingId"
        :data-bs-parent="`#${accordionId}`"
      >
        <div class="accordion-body bg-transparent">
          <p class="fs-6">Текст результата</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useId } from "vue";

const accordionId = `accordion-${useId()}`;
const headingId = `heading-${useId()}`;
const collapseId = `collapse-${useId()}`;
</script>
