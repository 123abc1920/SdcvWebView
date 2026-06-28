<template>
  <div class="accordion bg-transparent mt-2 mb-2" :id="accordionId">
    <div
      class="accordion-item mb-2"
      v-for="(item, index) in results"
      :key="index"
    >
      <h2 class="accordion-header" :id="headingId + index">
        <button
          class="accordion-button collapsed py-1 bg-transparent"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="`#${collapseId + index}`"
          aria-expanded="false"
          :aria-controls="collapseId + index"
        >
          {{ item.dict }}
        </button>
      </h2>

      <div
        :id="collapseId + index"
        class="accordion-collapse collapse"
        :aria-labelledby="headingId + index"
        :data-bs-parent="`#${accordionId}`"
      >
        <div class="accordion-body bg-transparent">
          <pre
            class="dict-text"
            v-html="sanitize(item.definition || item)"
          ></pre>
        </div>
      </div>
      <hr class="border-top border-2 border-primary my-2 w-100" />
    </div>
  </div>
</template>

<script setup>
import { useId } from "vue";
import DOMPurify from "dompurify";

defineProps({
  results: {
    type: Array,
    default: () => [],
  },
});

const accordionId = `accordion-${useId()}`;
const headingId = `heading-${useId()}`;
const collapseId = `collapse-${useId()}`;

const sanitize = (rawText) => {
  if (typeof rawText !== "string") return rawText;

  return DOMPurify.sanitize(rawText, {
    ALLOWED_TAGS: [
      "br",
      "b",
      "strong",
      "i",
      "em",
      "p",
      "div",
      "font",
      "u",
      "sub",
      "sup",
      "ul",
      "ol",
      "li",
      "table",
      "tr",
      "td",
      "rref",
      "a",
    ],
    ALLOWED_ATTR: ["color", "size", "href", "target"],
    ALLOW_UNKNOWN_PROTOCOLS: false,
  });
};
</script>

<style scoped>
.dict-text {
  white-space: pre-wrap;
}

.dict-text :deep(t) {
  font-weight: bold;
}
</style>
