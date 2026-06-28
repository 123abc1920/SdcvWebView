<template>
  <div
    class="rounded d-flex flex-row bg-primary align-items-center p-3 border border-1 border-primary mb-2"
  >
    <p class="fs-5 text-start m-0 text-light">{{ item.word }}</p>

    <button
      type="button"
      class="btn-close btn-sm btn-close-white ms-auto"
      aria-label="Удалить"
      @click.stop="deleteItem"
    ></button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Cookies from "js-cookie";

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["itemDeleted"]);

const deleteItem = async () => {
  const jwt = Cookies.get("jwt");

  if (jwt) {
    try {
      const response = await fetch("http://127.0.0.1:5200/delete/history", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${jwt}`,
        },
        body: JSON.stringify({
          ids: [props.item.id],
        }),
      });

      if (response.status === 200) {
        emit("itemDeleted", props.item.id);
      }
    } catch (error) {
      console.error("Ошибка:", error);
    }
  }
};
</script>
