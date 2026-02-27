<template>
<div class="min-h-[83vh] md:h-[83vh] bg-zinc-700 text-zinc-200 flex flex-col px-4 py-6 w-full overflow-auto md:overflow-hidden">

  <!-- HEADER -->
  <div class="flex flex-col sm:flex-row justify-between items-center mb-6 gap-4 px-4 flex-shrink-0">
    <h1 class="text-2xl sm:text-3xl font-bold text-red-500 text-center sm:text-left">
      Be To Do
      <span class="text-zinc-400 text-lg block sm:inline">
        — {{ user }}
      </span>
    </h1>

    <button 
      @click="cerrar"
      class="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg font-semibold transition"
    >
      Cerrar sesión
    </button>
  </div>


  <!-- CONTENEDOR PRINCIPAL: DOS COLUMNAS EN DESKTOP -->
  <div class="flex flex-col md:flex-row flex-1 gap-6 px-4 md:min-h-0 w-full">
    
    <!-- LISTA TAREAS (Izquierda) -->
    <div class="flex-1 bg-zinc-900 rounded-2xl shadow-2xl p-6 flex flex-col md:min-h-0 min-h-fit">

      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold text-red-500">
          MIS TAREAS
        </h2>
        <button
          v-if="tareas.length > 0"
          @click="eliminarTodasLasTareas"
          class="text-xs bg-red-800 hover:bg-red-700 text-red-300 px-3 py-1 rounded-lg font-semibold transition"
        >
          Limpiar todo
        </button>
      </div>

      <span v-if="tareas.length === 0" class="text-zinc-500">
        No tienes tareas pendientes :)
      </span>

      <!-- Scroll interno si hay muchas -->
      <div v-else class="space-y-4 overflow-y-auto pr-2 flex-1 min-h-0">

        <div
          v-for="tarea in tareas"
          :key="tarea.id_tarea"
          class="bg-zinc-800 rounded-xl p-4
                 hover:shadow-lg transition
                 flex flex-col gap-3"
        >

          <!-- INFO Y ESTADO -->
          <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3">
            <div>
              <p class="font-semibold text-lg" :class="tarea.estado === 'completada' ? 'text-green-400' : 'text-red-400'">
                {{ tarea.titulo }}
              </p>

              <p class="text-sm text-zinc-400 mt-1">
                {{ tarea.descripcion }}
              </p>

              <p class="text-xs text-zinc-600 mt-2">
                ID: {{ tarea.id_tarea }}
              </p>
            </div>

            <!-- ESTADO -->
            <span
              class="text-xs font-semibold px-3 py-1 rounded-full text-center"
              :class="{
                'bg-yellow-900 text-yellow-400': tarea.estado === 'pendiente',
                'bg-blue-900 text-blue-400': tarea.estado === 'en_marcha',
                'bg-green-900 text-green-400': tarea.estado === 'completada'
              }"
            >
              {{ tarea.estado == "en_marcha"
                ? "En marcha"
                : tarea.estado == "completada"
                ? "Completada"
                : "Pendiente"
              }}
            </span>
          </div>

          <!-- BOTÓN DE ELIMINACIÓN -->
          <div class="flex gap-2">
            <button
              @click="editarTarea(tarea)"
              class="flex-1 bg-blue-900 hover:bg-blue-800 text-blue-300 py-1 px-3 rounded-lg font-semibold transition text-sm"
            >
              ✏️ Editar
            </button>
            <button
              @click="eliminarTarea(tarea.id_tarea, tarea.titulo)"
              class="flex-1 bg-red-900 hover:bg-red-800 text-red-300 py-1 px-3 rounded-lg font-semibold transition text-sm"
            >
              🗑️ Eliminar
            </button>
          </div>

        </div>

      </div>
    </div>


    <!-- FORMULARIO (Derecha) -->
    <form
      @submit.prevent="postTareas"
      class="w-full md:w-96 bg-zinc-900 rounded-2xl shadow-2xl p-6 space-y-4 flex flex-col md:flex-shrink-0 md:overflow-y-auto md:max-h-[calc(100vh-180px)]"
    >
      <span class="block text-center text-lg font-semibold mb-4 text-red-500">
        Añadir nueva tarea
      </span>

      <div>
        <label class="block text-sm text-zinc-400 mb-1">
          Título
        </label>
        <input
          type="text"
          v-model="tarea"
          class="w-full bg-zinc-800 rounded-lg px-3 py-2
                 focus:outline-none focus:ring-2 focus:ring-red-600
                 text-zinc-200"
        >
      </div>

      <div>
        <label class="block text-sm text-zinc-400 mb-1">
          Descripción
        </label>
        <input
          type="text"
          v-model="descripcionTarea"
          class="w-full bg-zinc-800 rounded-lg px-3 py-2
                 focus:outline-none focus:ring-2 focus:ring-red-600
                 text-zinc-200"
        >
      </div>

      <div>
        <label class="block text-sm text-zinc-400 mb-1">
          Estado
        </label>
        <select
          v-model="estadoTarea"
          class="w-full bg-zinc-800 rounded-lg px-3 py-2
                 focus:outline-none focus:ring-2 focus:ring-red-600
                 text-zinc-200"
        >
          <option value="pendiente">Pendiente</option>
          <option value="en_marcha">En marcha</option>
          <option value="completada">Completada</option>
        </select>
      </div>

      <button
        class="w-full bg-red-600 hover:bg-red-700 py-2 rounded-lg font-semibold transition"
      >
        Añadir tarea
      </button>

      <!-- POMODORO TEMPORIZADOR -->
      <div class="border-t border-zinc-700 pt-6 mt-6">
        <h3 class="text-lg font-semibold text-red-500 text-center mb-4">
          POMODORO
        </h3>

        <!-- Selector de tarea -->
        <div class="mb-4">
          <label class="block text-sm text-zinc-400 mb-2">
            Selecciona una tarea
          </label>
          <select
            v-model="tareaPomodoro"
            class="w-full bg-zinc-800 rounded-lg px-3 py-2
                   focus:outline-none focus:ring-2 focus:ring-red-600
                   text-zinc-200"
          >
            <option value="">-- Elige una tarea --</option>
            <option v-for="t in tareas.filter(t => t.estado !== 'completada')" :key="t.id_tarea" :value="t.id_tarea">
              {{ t.titulo }}
            </option>
          </select>
        </div>

        <!-- Temporizador visible -->
        <div class="bg-zinc-800 rounded-lg p-4 text-center mb-4">
          <div class="text-4xl font-bold font-mono" :class="enDescanso ? 'text-green-500' : 'text-red-500'">
            {{ formatoTiempo(tiempoRestante) }}
          </div>
          <p class="text-xs text-zinc-400 mt-2">
            {{ enDescanso ? "☕ Tiempo de descanso" : pomodoroActivo ? "⏱️ En progreso..." : "Listo para comenzar" }}
          </p>
        </div>

        <!-- Botones de control -->
        <button
          @click="iniciarPomodoro"
          v-if="!pomodoroActivo && !enDescanso"
          :disabled="!tareaPomodoro"
          class="w-full bg-green-600 hover:bg-green-700 disabled:bg-zinc-600 py-2 rounded-lg font-semibold transition mb-2"
        >
          Iniciar Pomodoro
        </button>

        <button
          @click="pausarPomodoro"
          v-else-if="pomodoroActivo && !enDescanso"
          class="w-full bg-yellow-600 hover:bg-yellow-700 py-2 rounded-lg font-semibold transition mb-2"
        >
          Pausar
        </button>

        <button
          @click="iniciarDescanso"
          v-if="pomodoroActivo && !enDescanso"
          class="w-full bg-purple-600 hover:bg-purple-700 py-2 rounded-lg font-semibold transition mb-2"
        >
          ☕ Necesito un café
        </button>

        <button
          @click="terminarDescanso"
          v-if="enDescanso"
          class="w-full bg-cyan-600 hover:bg-cyan-700 py-2 rounded-lg font-semibold transition mb-2"
        >
          ✓ Ya he descansado
        </button>

        <button
          @click="completarTareaPomodoro"
          v-if="tareaPomodoro && !enDescanso"
          class="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded-lg font-semibold transition"
        >
          ✓ Tarea Completada
        </button>
      </div>

    </form>

  </div>

</div>
</template>


<script setup>
import { ref, onMounted, watch } from "vue"
import axios from "axios"

import { useRouter } from "vue-router"
const user = ref("")
const tarea = ref("")
const descripcionTarea = ref("")
const estadoTarea = ref("pendiente")
const tareas = ref([])
const router = useRouter()

// POMODORO
const tareaPomodoro = ref("")
const pomodoroActivo = ref(false)
const enDescanso = ref(false)
const tiempoRestante = ref(1500) // 25 minutos en segundos
const tiempoDescanso = 300 // 5 minutos en segundos
const intervaloPomodoro = ref(null)

// Watch para reiniciar temporizador cuando cambia la tarea
watch(tareaPomodoro, (newValue) => {
  if (newValue) {
    pausarPomodoro()
    enDescanso.value = false
    tiempoRestante.value = 1500
  }
})

const formatoTiempo = (segundos) => {
  const minutos = Math.floor(segundos / 60)
  const secs = segundos % 60
  return `${String(minutos).padStart(2, "0")}:${String(secs).padStart(2, "0")}`
}

const iniciarPomodoro = () => {
  if (!tareaPomodoro.value) return
  pomodoroActivo.value = true
  
  intervaloPomodoro.value = setInterval(() => {
    tiempoRestante.value--
    if (tiempoRestante.value <= 0) {
      pausarPomodoro()
    }
  }, 1000)
}

const pausarPomodoro = () => {
  pomodoroActivo.value = false
  if (intervaloPomodoro.value) {
    clearInterval(intervaloPomodoro.value)
  }
}

const iniciarDescanso = () => {
  pausarPomodoro()
  enDescanso.value = true
  tiempoRestante.value = tiempoDescanso
  
  intervaloPomodoro.value = setInterval(() => {
    tiempoRestante.value--
    if (tiempoRestante.value <= 0) {
      terminarDescansoAutomatico()
    }
  }, 1000)
}

const terminarDescanso = () => {
  if (intervaloPomodoro.value) {
    clearInterval(intervaloPomodoro.value)
  }
  enDescanso.value = false
  tiempoRestante.value = 1500
}

const terminarDescansoAutomatico = () => {
  if (intervaloPomodoro.value) {
    clearInterval(intervaloPomodoro.value)
  }
  enDescanso.value = false
  tiempoRestante.value = 1500
  pausarPomodoro()
  // Mostrar notificación
  alert("¡Descanso terminado! Tiempo de volver al trabajo 💪")
}

const completarTareaPomodoro = async () => {
  try {
    if (!tareaPomodoro.value) return
    
    // Obtener la tarea para actualizar su estado
    const tareaObj = tareas.value.find(t => t.id_tarea === tareaPomodoro.value)
    if (!tareaObj) return
    
    // La ruta PUT ahora acepta título/descripcion/estado, pero solo cambiamos el estado
    const res = await axios.put(`http://localhost:5000/auth/tareas/${tareaPomodoro.value}`, {
      estado: "completada"
    }, {
      withCredentials: true
    })
    
    console.log("Tarea completada:", res.data)
    pausarPomodoro()
    tareaPomodoro.value = ""
    tiempoRestante.value = 1500
    enDescanso.value = false
    await getTareas()
  } catch (error) {
    console.error("Error al completar tarea:", error.response?.data || error.message)
  }
}

const editarTarea = async (tarea) => {
  // prompts for new values, allow cancel
  const nuevoTitulo = prompt("Nuevo título:", tarea.titulo)
  if (nuevoTitulo === null) return // user cancelled

  const nuevaDesc = prompt("Nueva descripción:", tarea.descripcion)
  if (nuevaDesc === null) return

  let nuevoEstado = prompt("Nuevo estado (pendiente/en_marcha/completada):", tarea.estado)
  if (nuevoEstado === null) return
  nuevoEstado = nuevoEstado.trim().toLowerCase()
  if (!["pendiente","en_marcha","completada"].includes(nuevoEstado)) {
    alert("Estado inválido")
    return
  }

  try {
    const res = await axios.put(`http://localhost:5000/auth/tareas/${tarea.id_tarea}`, {
      titulo: nuevoTitulo,
      descripcion: nuevaDesc,
      estado: nuevoEstado
    }, {
      withCredentials: true
    })
    console.log("Tarea actualizada:", res.data)
    await getTareas()
  } catch (error) {
    console.error("Error al editar tarea:", error.response?.data || error.message)
    alert("No se pudo actualizar la tarea")
  }
}

const eliminarTarea = async (tareaId, nombreTarea) => {
  const confirmacion = confirm(`¿Estás seguro de querer eliminar la tarea "${nombreTarea}"?`)
  if (!confirmacion) return

  try {
    const res = await axios.delete(`http://localhost:5000/auth/tareas/${tareaId}`, {
      withCredentials: true
    })
    console.log("Tarea eliminada:", res.data)
    await getTareas()
  } catch (error) {
    console.error("Error al eliminar tarea:", error.response?.data || error.message)
    alert("Error al eliminar la tarea")
  }
}

const eliminarTodasLasTareas = async () => {
  const confirmacion = confirm(`¿Estás seguro de querer eliminar TODAS las tareas? Esta acción no se puede deshacer.`)
  if (!confirmacion) return

  try {
    const res = await axios.delete(`http://localhost:5000/auth/tareas`, {
      withCredentials: true
    })
    console.log("Todas las tareas eliminadas:", res.data)
    await getTareas()
  } catch (error) {
    console.error("Error al eliminar todas las tareas:", error.response?.data || error.message)
    alert("Error al eliminar las tareas")
  }
}

// Limpiar intervalo al desmontar
onMounted(() => {
  return () => {
    if (intervaloPomodoro.value) {
      clearInterval(intervaloPomodoro.value)
    }
  }
})

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
         console.log("tareas", tareas.value)
       }
    } catch (error) {
        console.error("Error al obtener tareas:", error.response?.data || error.message)
    }
}

const postTareas = async() =>{
    try {
        // simple client-side sanitize (strip tags)
        const clean = str => str.replace(/<[^>]*>?/gm, '')
        const payload = {
          titulo: clean(tarea.value),
          descripcion: clean(descripcionTarea.value),
          estado: estadoTarea.value
        }

        const res = await axios.post("http://localhost:5000/auth/tareas", payload, {
          withCredentials: true
        })
        console.log("Tarea creada:", res.data)
        tarea.value = ""
        descripcionTarea.value = ""
        estadoTarea.value = "pendiente"
        await getTareas()
    } catch (error) {
        console.error("Error al crear tarea:", error.response?.data || error.message)
    }
}

onMounted(async () => {
    const storedUser = localStorage.getItem("USER_ID")
    if (storedUser) {
      try {
        const userData = JSON.parse(storedUser)
        user.value = userData.email || userData
      } catch {
        // Si no es JSON válido, usarlo directamente
        user.value = storedUser
      }
    }
    await getTareas()
})
    
</script>

<style lang="sass" scoped>

</style>