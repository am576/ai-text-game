<template>
  <div class="homepage bg-slate-800 h-screen flex flex-col items-center">
	<h1 class="text-5xl py-10 font-bold text-slate-200 text-center">Choose your adventure</h1>
	<div class="adventures-list flex justify-between w-2/3 flex-wrap -mx-2">
		<div class="adventure w-1/3 relative flex flex-col px-4 mb-8" v-for="adventure in adventures" :key="adventure.id">
			<h3 class="text-3xl text-center absolute top-5 w-full"></h3>
			<img :src="previewUrl(adventure.id)" style="object-fit: contain;" class="self-start">
			<div class="adventure-info w-full flex flex-col gap-2 relative" :style="`background-image: url(${previewUrl(adventure.id)})`">
				<span class="adventure-name merriweather">{{ adventure.name }}</span>
				<span class="adventure-description roboto">{{ adventure.description }}</span>
			</div>
		</div>
	</div>
	<h1 class="text-5xl py-10 font-bold text-slate-200 text-center">or <router-link to="/create_adventure" class="link">create</router-link> a new one</h1>
</div>
</template>

<script>
	import axios from 'axios';

	export default {
		setup () {
		},
		data() {    
			return {
			adventures: [],
		}
		},
		methods: {
			getAdventures() {
				const url = process.env.VUE_APP_BACKEND_URL
				axios.get(`${url}/get_adventures`)
				.then(response => {
					this.adventures = response.data
				})
			},
			previewUrl(adventure_id) {
				return require(`../assets/adventures/${adventure_id}/preview.png`);
			},
		},
		created() {
			this.getAdventures()
		},
		computed: {
			
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

.adventure-info {
	padding: 20px;
	height: 150px;
	span {
		@apply text-white;
		z-index: 10;
	}
	.adventure-name {
		font-size: 24px;
		font-weight: bold;
	}
	.adventure-description {
		font-size: 18px;
		line-height: 22px;
	}
}

.adventure-info::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  backdrop-filter: blur(30px);
  background-color: rgba(0, 0, 0, 0.54);
}
</style>