<template>
  <div class="w-full max-w-2xl mx-auto p-6">
    <header class="mb-6">
      <h1 class="text-3xl font-bold">Contacto</h1>
      <p class="text-gray-600 mt-2">¿Tienes preguntas o sugerencias? Escríbenos.</p>
    </header>

    <form @submit.prevent="handleSubmit" class="bg-white p-6 rounded shadow">
      <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Nombre</label>
        <input v-model="form.name" type="text" class="w-full border rounded px-3 py-2" required />
      </div>

      <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Email</label>
        <input v-model="form.email" type="email" class="w-full border rounded px-3 py-2" required />
      </div>

      <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Mensaje</label>
        <textarea v-model="form.message" rows="5" class="w-full border rounded px-3 py-2" required></textarea>
      </div>

      <div class="text-right">
        <button type="submit" class="bg-[#ff5252] text-white px-4 py-2 rounded">Enviar</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useToast } from 'vue-toastification'

const toast = useToast()
const form = reactive({ name: '', email: '', message: '' })

function handleSubmit() {
  // Aquí normalmente enviarías al backend. Mostramos un toast de éxito.
  toast.success('Mensaje enviado. Gracias por contactarnos.')
  form.name = ''
  form.email = ''
  form.message = ''
}
</script>

<style scoped>
</style>
