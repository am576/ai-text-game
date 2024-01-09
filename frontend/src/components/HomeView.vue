<template>
  <div class="homepage bg-slate-800 h-screen flex flex-col items-center">
	<h1 class="text-5xl py-10 font-bold text-slate-200 text-center">Choose your adventure</h1>
	<adventures-list></adventures-list>
	<h1 class="text-5xl py-10 font-bold text-slate-200 text-center">or <router-link to="/create_adventure" class="link">create</router-link> a new one</h1>
</div>
</template>

<script>
	export default {
		
	}
</script>

<style lang="scss" scoped>
.link {
  @apply text-sky-600
  
}
.link:hover {
  @apply underline
}


</style>