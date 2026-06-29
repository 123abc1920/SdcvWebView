<template>
  <div
    class="offcanvas offcanvas-end text-bg-light"
    tabindex="-1"
    id="offcanvasSettings"
    aria-labelledby="offcanvasSettingsLabel"
  >
    <div class="offcanvas-header border-bottom">
      <h5 class="offcanvas-title fw-bold" id="offcanvasSettingsLabel">
        <i class="bi bi-gear-fill mx-2"></i> Настройки
      </h5>
      <button
        type="button"
        class="btn-close"
        data-bs-dismiss="offcanvas"
        aria-label="Закрыть"
      ></button>
    </div>

    <div class="offcanvas-body">
      <p>Выберите, где sdcv:</p>

      <div class="form-check">
        <input
          class="form-check-input"
          type="radio"
          name="sdcvRadio"
          id="dockerRadio"
          value="docker"
          v-model="sdcvType"
        />
        <label class="form-check-label" for="dockerRadio">
          Sdcv in Docker
        </label>
      </div>
      <div id="container" v-if="isContainerVisible" class="my-2">
        <input
          type="text"
          class="form-control fs-5 rounded"
          placeholder="Имя контейнера"
          v-model="containerName"
          @input="containerInput"
        />
      </div>
      <div class="form-check">
        <input
          class="form-check-input"
          type="radio"
          name="sdcvRadio"
          id="linuxRadio"
          value="linux"
          v-model="sdcvType"
          checked
        />
        <label class="form-check-label" for="linuxRadio"> Sdcv in Linux </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import Cookies from "js-cookie";

const sdcvType = ref("linux");
const isContainerVisible = ref(false);
const containerName = ref("");

const containerInput = () => {
  Cookies.set("containerName", containerName.value, { expires: 365 });
};

onMounted(async () => {
  const savedType = Cookies.get("sdcvType");
  if (savedType) {
    sdcvType.value = savedType;
    Cookies.set("sdcvType", savedType, { expires: 365 });
    if (savedType === "docker") {
      isContainerVisible.value = true;
    }
  } else {
    Cookies.set("sdcvType", sdcvType.value, { expires: 365 });
  }

  const savedContainer = Cookies.get("containerName");
  if (savedContainer) {
    containerName.value = savedContainer;
  }
});

watch(sdcvType, (newValue) => {
  Cookies.set("sdcvType", newValue, { expires: 365 });
  if (newValue === "docker") {
    isContainerVisible.value = true;
    const savedContainer = Cookies.get("containerName");
    if (savedContainer) {
      containerName.value = savedContainer;
    }
  } else if (newValue === "linux") {
    isContainerVisible.value = false;
  }
});
</script>
