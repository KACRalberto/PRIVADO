
<template>
  <div class="w-full max-w-md mx-auto p-6">
    <h1 class="text-2xl font-bold mb-4">Restablecer contraseña</h1>

    <form @submit.prevent="handleReset" class="bg-white p-6 rounded shadow">
      <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Nueva contraseña</label>
        <input v-model="password" type="password" class="w-full border rounded px-3 py-2" required />
      </div>

      <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Confirmar contraseña</label>
        <input v-model="password2" type="password" class="w-full border rounded px-3 py-2" required />
      </div>

      <div class="text-right">
        <button type="submit" class="bg-[#ff5252] text-white px-4 py-2 rounded">Cambiar contraseña</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const token = route.query.token || ''
const password = ref('')
const password2 = ref('')

async function handleReset(){
  if(password.value !== password2.value){
    toast.error('Las contraseñas no coinciden')
    return
  }

  try{
    const resp = await axios.post('http://localhost:5000/auth/reset-password', { token, password: password.value })
    if(resp.status === 200){
      toast.success('Contraseña actualizada. Ya puedes iniciar sesión.')
      router.push('/login')
    }
  }catch(err){
    console.error(err)
    if(err.response && err.response.data && err.response.data.error){
      toast.error(err.response.data.error)
    }else{
      toast.error('Error al restablecer la contraseña')
    }
  }
}
</script>

<style scoped>
</style>
