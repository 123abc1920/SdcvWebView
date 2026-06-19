<template>
  <div class="d-flex flex-column min-vh-100">
    <Header />

    <Content />

    <Footer />

    <SettingsOffcanvas />
    <HistoryOffcanvas />
    <LoginModal />
  </div>
</template>

<script setup>
import { ref } from "vue";

import SettingsOffcanvas from "./settings_offcanvas.vue";
import HistoryOffcanvas from "./history_offcanvas.vue";
import LoginModal from "./login_modal.vue";
import Header from "./header.vue";
import Footer from "./footer.vue";
import Content from "./content.vue";
</script>
