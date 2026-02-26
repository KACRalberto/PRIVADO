<template>
  <section class="flex p-4 items-center justify-center">
    <div class="w-85 max-w-md px-6 lg:w-150">
      <form
        @submit.prevent=""
        class="bg-white shadow-xl rounded-2xl p-8 flex flex-col gap-6"
      >
        <!-- Título -->
        <h2 class="text-2xl font-bold text-center text-gray-700">
          Registro
        </h2>

        <!-- Apodo -->
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-600">Apodo</label>
          <input
            type="text"
            class="border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            v-model="apodo"
          />
        </div>

        <!-- Email -->
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-600">Email</label>
          <input
            type="email"
            class="border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            v-model="email_user"
          />
        </div>

        <!-- Contraseña -->
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-600">Contraseña</label>
          <input
            type="password"
            class="border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            v-model="password_user"
          />
        </div>

        <!-- Repetir contraseña -->
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-600">
            Repetir contraseña
          </label>
          <input
            type="password"
            class="border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            v-model="password_user_confirm"
          />
        </div>

        <!-- Botón -->
        <ButtonsLoginRegister
          content="REGISTRARME"
          class="mt-4 w-45 self-center bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition"
          @click="do_register"
        />

        <router-link to="/login">¿Ya tienes cuenta? <span class="text-[#ff5252]">Inicia sesión</span></router-link>
      </form>
    </div>
  </section>
</template>


<script setup>
import ButtonsLoginRegister from '@/components/ButtonsLoginRegister.vue';
import { ref } from 'vue';
import axios from 'axios';
import { useToast } from "vue-toastification";
import { useRouter } from 'vue-router';
const toast = useToast()
const router = useRouter()
let apodo = ref("")
let email_user = ref("")
let password_user = ref("")
let password_user_confirm = ref("")
let all_right = ref(false)

const do_register = async()=>{
  // client-side remove any html tags
  const clean = str => str.replace(/<[^>]*>?/gm, '')

  console.log(apodo.value,email_user.value,password_user.value, password_user_confirm.value)
  if(password_user.value == password_user_confirm.value){
    all_right.value = true
  }else{
    toast.error("LAS CONTRASEÑAS DEBEN COINCIDIR", {
                position: "bottom-center",
                timeout: 3009,
                closeOnClick: true,
                pauseOnFocusLoss: false,
                pauseOnHover: false,
                draggable: true,
                draggablePercent: 0.6,
                showCloseButtonOnHover: false,
                hideProgressBar: true,
                closeButton: "button",
                icon: false,
                rtl: false,
              });
  }

  if(all_right.value){
    try{
      const response = await axios.post("http://localhost:5000/auth/register",{
        email: clean(email_user.value),
        name: clean(apodo.value),
        password: password_user.value,
        password_check: password_user_confirm.value
      }, {
        withCredentials: true
      })
      if(response.status === 200){
        toast.success("Usuario registrado correctamente", {
                position: "bottom-center",
                timeout: 3009,
                closeOnClick: true,
                pauseOnFocusLoss: false,
                pauseOnHover: false,
                draggable: true,
                draggablePercent: 0.6,
                showCloseButtonOnHover: false,
                hideProgressBar: true,
                closeButton: "button",
                icon: false,
                rtl: false,
              })
        localStorage.setItem("TOKEN", response.data.token)
        localStorage.setItem("USER_ID", response.data.user)
        router.push("/home")
      }

    }catch(error){
      if(error.response){
        if (error.response.status == 409){
          toast.error("Usuario ya registrado", {
                position: "bottom-center",
                timeout: 3009,
                closeOnClick: true,
                pauseOnFocusLoss: false,
                pauseOnHover: false,
                draggable: true,
                draggablePercent: 0.6,
                showCloseButtonOnHover: false,
                hideProgressBar: true,
                closeButton: "button",
                icon: false,
                rtl: false,
              })
        }
        else if(error.response.status == 400){
          toast.info("Email y contraseña obligatorios", {
                position: "bottom-center",
                timeout: 3009,
                closeOnClick: true,
                pauseOnFocusLoss: false,
                pauseOnHover: false,
                draggable: true,
                draggablePercent: 0.6,
                showCloseButtonOnHover: false,
                hideProgressBar: true,
                closeButton: "button",
                icon: false,
                rtl: false,
              })
        }
        else{
          toast.error("Error interno del servidor ;(", {
                position: "bottom-center",
                timeout: 3009,
                closeOnClick: true,
                pauseOnFocusLoss: false,
                pauseOnHover: false,
                draggable: true,
                draggablePercent: 0.6,
                showCloseButtonOnHover: false,
                hideProgressBar: true,
                closeButton: "button",
                icon: false,
                rtl: false,
              })
        }
      }
      else{
        toast.error("Error interno del servidor ;(", {
                position: "bottom-center",
                timeout: 3009,
                closeOnClick: true,
                pauseOnFocusLoss: false,
                pauseOnHover: false,
                draggable: true,
                draggablePercent: 0.6,
                showCloseButtonOnHover: false,
                hideProgressBar: true,
                closeButton: "button",
                icon: false,
                rtl: false,
              })
      }
    }
  }
  
}


</script>

<style lang="sass" scoped>

</style>