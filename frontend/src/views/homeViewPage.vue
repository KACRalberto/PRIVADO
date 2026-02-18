<template>
    <section class="w-full flex flex-col mt-2">
        <h1 class="self-center text-2xl font-[Poppins] font-semibold">
            ¡¡Bienvenido a BeToDo!!
        </h1>

        <transition enter-active-class="animate__animated animate__fadeInLeft" leave-active-class="animate__animated animate__fadeOutLeft">
            <h2 v-if="valor" class="self-center text-xl font-[Poppins] font-bold absolute mt-10 text-center px-5">
                Aqui podrás apuntar tus deberes, tareas y cosas pendientes de tu día a día 😁
            </h2>
        </transition>

        <div id="primera-vista" class="flex flex-col self-start w-full justify-center p-10 lg:mt-15 mt-35">
            <div class="flex flex-col text-[black] font-[700] font-[Poppins] lg:text-5xl text-2xl mb-5 md:text-4xl lg:self-center lg:text-center lg:pb-5">
                <h1>
                    <span class="text-red-500">
                        ORGANIZA
                    </span>
                     TU DÍA</h1>
                <h3>PLANIFICA 

                    <span class="text-red-500">
                        SIN ESTRÉS
                    </span>
                </h3>
            </div>
            <p class="font-[Poppins] text-[black] font-[600] lg:text-xl lg:self-center lg:text-center">
                BeToDo organiza tus tareas diarias, proyectos y recordatorios en un solo lugar.
                <br>
                Planifica, prioriza y completa objetivos fácilmente con una app simple, rápida y confiable 
                <br>
                para tu productividad diaria personal.
            </p>
            <router-link to="/register" class="w-55 mt-5  lg:self-center lg:w-90 lg:h-15 flex justify-center items-center REGISTER">¿Comenzamos?</router-link>
            <router-link to="/login" class="w-60 mt-5 lg:self-center LOGIN font-[700]">¿Ya tienes cuenta? 
            <span class="text-blue-500 font-[900]">
                Inicia sesión.
            </span>
            </router-link>

        </div>

        <div id="pomodoro" class="lg:w-full flex lg:justify-center flex-col lg:text-start items-center text-center pt-10 lg:flex-row">
            <img class="rounded-[12%] lg:w-[700px] w-[450px]" src="../assets/IMG/PNGPORTATIL.png" alt="">
            <p class="lg:w-120 p-3 font-[Poppins] font-[400] self-center lg:text-3xl text-[16px]">
                    La técnica Pomodoro es un método de estudio que divide el tiempo en bloques de 25 minutos de concentración, seguidos de breves descansos.
                    <br><br>
                    Ayuda a mejorar el enfoque, evitar distracciones y estudiar de forma más eficiente y sostenible.
            </p>
        </div>
            
       
        <div class="text-3xl font-[Poppins] flex flex-col p-5 lg:flex lg:flex-row text-center lg:text-end lg:gap-10 gap-5 items-center justify-center py-10">
            <p class="text-sm sm:text-sm text-[16px] lg:text-3xl lg:w-[900px]">
                En 
                <span class="text-red-500 font-medium">
                    BeToDo
                </span>
                , cada tarea puede gestionarse siguiendo la técnica Pomodoro. Solo elige una tarea, activa los bloques de 25 minutos de enfoque y 5 minutos de descanso, y aprovecha tu tiempo de manera más eficiente. ¡Tú decides cuándo y cómo usar 
                <span class="text-red-500 font-medium">
                    Pomodoro
                </span>
                ! 🍅
            </p>
            <img src="../assets/IMG/TOMATOBETO.png" class="lg:w-60 w-25" alt="">
        </div>
    </section>
</template>

<script setup>

    import { ref } from 'vue';
    let valor = ref(false)
    setTimeout(() => {
        valor.value = true
    }, 1000);

</script>

<style lang="sass" scoped>
#primera-vista
  height: 500px
  background: linear-gradient(
      rgba(254,245,239,0.7),
      rgba(254,245,239,0.7)
    ), url("@/assets/IMG/FNDO.png")
  background-size: cover
  background-position: center
  background-repeat: no-repeat
.REGISTER
  padding: 1px 2px
  font-size: 24px
  font-weight: bold
  text-align: center
  text-decoration: none
  color: #fff
  background-color: #ff5252
  border: 2px solid #000
  border-radius: 10px
  box-shadow: 5px 5px 0px #000
  transition: all 0.3s ease
  cursor: pointer
  outline: none 

  &:hover
    background-color: #fff
    color: #ff5252
    border: 2px solid #ff5252
    box-shadow: 5px 5px 0px #ff5252

  &:active
    background-color: #fcf414
    box-shadow: none
    transform: translateY(4px)
.LOGIN
    font-size: 15px

</style>
