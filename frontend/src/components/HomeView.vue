<template>
    <div class="homepage bg-slate-800 h-screen flex flex-col items-center">
		<h1 class="text-5xl py-10 font-bold text-slate-200 text-center">Choose your adventure</h1>
		<div class="adventures-list flex justify-between w-2/3 gap-8">
			<div class="w-full h-full relative">
				<h3 class="text-3xl text-center absolute top-5 w-full">Adventure 1</h3>
				<img src="http://via.placeholder.com/512x512" >
			</div>
			<div class="w-full h-full relative">
				<h3 class="text-3xl text-center absolute top-5 w-full">Adventure 1</h3>
				<img src="http://via.placeholder.com/512x512" >
			</div>
			<div class="w-full h-full relative">
				<h3 class="text-3xl text-center absolute top-5 w-full">Adventure 1</h3>
				<img src="http://via.placeholder.com/512x512" >
			</div>
		</div>
		<h1 class="text-5xl py-10 font-bold text-slate-200 text-center">or <router-link to="/create_adventure" class="link">create</router-link> a new one</h1>
	</div>
</template>

<script>
export default {
    setup () {

    },
    data() {    
        return {}
    }
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