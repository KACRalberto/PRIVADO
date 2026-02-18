<script setup>
import FooterForAllPages from './components/FooterForAllPages.vue';
import HeaderForAllPages from './components/HeaderForAllPages.vue'
</script>


<template >

  <div class="flex flex-col min-h-screen">
    <HeaderForAllPages />
    <main class="flex-1 flex items-center justify-center">
      <router-view />
    </main>
    <FooterForAllPages class=""/>
  </div>

</template>

<style lang="sass" scoped>
main
  height: 100%
</style>
