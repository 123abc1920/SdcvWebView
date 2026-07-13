<template>
  <div class="accordion bg-transparent mt-2 mb-2" id="resultsAccordion">
    <div
      class="accordion-item mb-2"
      v-for="(item, index) in results"
      :key="index"
    >
      <h2 class="accordion-header" :id="`heading-${index}`">
        <button
          class="accordion-button py-1 bg-transparent"
          :class="{ collapsed: activeIndex !== index }"
          type="button"
          @click="toggleItem(index)"
          :aria-expanded="activeIndex === index ? 'true' : 'false'"
          :aria-controls="`collapse-${index}`"
        >
          {{ item.dict_title }}
        </button>
      </h2>

      <div
        :id="`collapse-${index}`"
        class="accordion-collapse collapse"
        :class="{ show: activeIndex === index }"
        :aria-labelledby="`heading-${index}`"
        data-bs-parent="#resultsAccordion"
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
import { ref } from "vue";
import DOMPurify from "dompurify";

defineProps({
  results: {
    type: Array,
    default: () => [],
  },
});

const activeIndex = ref(-1);

const toggleItem = (index) => {
  if (activeIndex.value === index) {
    activeIndex.value = -1;
  } else {
    activeIndex.value = index;
  }
};

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
