<template>
<div class="min-h-screen bg-gray-100 flex flex-col justify-center items-center px-4">
  
  <h1 class="text-3xl font-bold text-indigo-600 mb-6">
    Bienvenido a Be To Do! 
    <span class="text-gray-700">{{ user }}</span>
  </h1>
  <button @click="cerrar">Cerrar sesión</button>

  <div class="w-full max-w-xl bg-white rounded-xl shadow-md p-6 mb-8 text-center">
    <h2 class="text-xl font-semibold mb-4">MIS TAREAS</h2>

    <span v-if="!tareas" class="text-gray-500">
      No tienes tareas pendientes :)
    </span>

<div v-else class="space-y-4">
  <div
    v-for="(tarea,index) in tareas"
    :key="index"
    class="bg-gray-50 border rounded-lg p-4 shadow-sm
           hover:shadow-md transition flex justify-between items-center"
  >
    <!-- Info tarea -->
    <div class="text-left">
      <p class="font-semibold text-lg text-gray-800">
        {{ tarea[2] }}
      </p>

      <p class="text-sm text-gray-500">
        {{ tarea[3] }}
      </p>

      <p class="text-xs text-gray-400 mt-1">
        Creada: {{ tarea[5] }}
      </p>
    </div>

    <!-- Estado -->
    <span
      class="text-xs font-semibold px-3 py-1 rounded-full"
      :class="{
        'bg-yellow-100 text-yellow-700': tarea[4] === 'pendiente',
        'bg-blue-100 text-blue-700': tarea[4] === 'en_marcha',
        'bg-green-100 text-green-700': tarea[4] === 'completada'
      }"
    >
      {{ tarea[4] }}
    </span>
  </div>
</div>

  </div>

  <form
    @submit.prevent="postTareas"
    class="w-full max-w-xl bg-white rounded-xl shadow-md p-6 space-y-4"
  >
    <span class="block text-center text-lg font-semibold mb-2">
      ¿Desea añadir una tarea?
    </span>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Tarea
      </label>
      <input
        type="text"
        placeholder="Nombre de la tarea"
        v-model="tarea"
        class="w-full border border-gray-300 rounded-lg px-3 py-2
               focus:outline-none focus:ring-2 focus:ring-indigo-400"
      >
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Descripción
      </label>
      <input
        type="text"
        placeholder="Descripción de la tarea"
        v-model="descripcionTarea"
        class="w-full border border-gray-300 rounded-lg px-3 py-2
               focus:outline-none focus:ring-2 focus:ring-indigo-400"
      >
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Estado
      </label>
      <select
        v-model="estadoTarea"
        class="w-full border border-gray-300 rounded-lg px-3 py-2
               focus:outline-none focus:ring-2 focus:ring-indigo-400"
      >
        <option value="pendiente">Tarea pendiente</option>
        <option value="en_marcha">En marcha</option>
        <option value="completada">Completada</option>
      </select>
    </div>

    <button
      class="w-full bg-indigo-600 text-white py-2 rounded-lg font-semibold
             hover:bg-indigo-700 transition duration-200"
    >
      Añadir tarea
    </button>
  </form>

</div>

</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import { useRouter } from "vue-router"
const user = ref("")
const tarea = ref("")
const descripcionTarea = ref("")
const estadoTarea = ref("pendiente")
const tareas = ref([])
const router = useRouter()

const cerrar = async()=>{
  try {
    const res = await axios.get("http://localhost:5000/auth/logout", {
      withCredentials: true
    })
    console.log(res)
    localStorage.removeItem("TOKEN")
    localStorage.removeItem("USER_ID")
    router.push("/")
  } catch (error) {
    console.error("Error al cerrar sesión:", error.response?.data || error.message)
  }
}


const getTareas = async()=>{
    try {
        const res = await axios.get("http://localhost:5000/auth/tareas", {
        withCredentials: true
        })
       console.log(res, "RES")
       if(res.data.ok){
        tareas.value = res.data.tareas
       }
    } catch (error) {
        console.error("Error al obtener tareas:", error.response?.data || error.message)
    }
}

const postTareas = async() =>{
    try {
        await axios.post("http://localhost:5000/auth/tareas", {
        titulo: tarea.value,
        descripcion: descripcionTarea.value,
        estado: estadoTarea.value
        }, {
        headers: {
            Authorization: "Bearer " + localStorage.getItem("TOKEN")
        }
        })
        console.log("Tarea creada:", resPost.data)
        tarea.value = ""
        descripcionTarea.value = ""
        estadoTarea.value = "pendiente"
        await getTareas()
    } catch (error) {
        console.error("Error al crear tarea:", error.response?.data || error.message)
    }
}

onMounted (()=>{
    const token = localStorage.getItem("TOKEN")
    user.value = JSON.parse(localStorage.getItem("USER_ID"))
    user.value = user.value.email
    getTareas()
  }
    )
    
</script>

<style lang="sass" scoped>

</style>