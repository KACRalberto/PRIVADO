<template>
  <div class="w-full max-w-2xl mx-auto p-6">
    <h1 class="text-2xl font-bold mb-4">Recuperar contraseña</h1>

    <form @submit.prevent="handleRequest" class="bg-white p-6 rounded shadow">
      <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Email</label>
        <input v-model="email" type="email" class="w-full border rounded px-3 py-2" required />
      </div>


      <div class="text-right">
        <button type="submit" class="bg-[#ff5252] text-white px-4 py-2 rounded">Enviar enlace de recuperación</button>
      </div>
    </form>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import emailjs from '@emailjs/browser'
import { useToast } from 'vue-toastification'

const toast = useToast()
const email = ref('')


// Prefer environment variables
const serviceId = import.meta.env.VITE_EMAILJS_SERVICE_ID || ''
const templateId = import.meta.env.VITE_EMAILJS_TEMPLATE_ID || ''
const publicKey = import.meta.env.VITE_EMAILJS_PUBLIC_KEY || ''

// no inputs: usamos directamente las vars de entorno

async function handleRequest(){
  try{
    const clean = str => str.replace(/<[^>]*>?/gm, '')
    const resp = await axios.post('http://localhost:5000/auth/request-password-reset', { email: clean(email.value) })
    if(resp.status === 200 && resp.data.token){
      const token = resp.data.token
      const resetUrl = `${window.location.origin}/reset-password?token=${token}`


      // decide credentials
      const sId = serviceId
      const tId = templateId
      const pKey = publicKey

      if(!sId || !tId || !pKey){
        toast.info('Token generado. Las credenciales de EmailJS no están configuradas; copia manualmente el enlace mostrado.', { timeout: 5000 })
        return
      }

      const templateParams = {
        to_email: email.value,
        link: resetUrl,
        app_name: 'BeToDo'
      }

      await emailjs.send(sId, tId, templateParams, pKey)
      toast.success('Correo enviado. Revisa tu bandeja de entrada.')

    }else{
      toast.info('Si existe la cuenta, se ha enviado un correo')
    }
  }catch(err){
    console.error(err)
    toast.error('Error al solicitar recuperación')
  }
}
</script>

<style scoped>
</style>
