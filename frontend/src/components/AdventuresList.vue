<template>
   <div class="adventures-list flex justify-between w-2/3 flex-wrap -mx-2">
		<div class="adventure w-1/3 relative flex flex-col px-4 mb-8" v-for="adventure in adventures" :key="adventure.id">
			<h3 class="text-3xl text-center absolute top-5 w-full"></h3>
			<img :src="previewUrl(adventure.id)" style="object-fit: contain;" class="self-start">
            <div>
                <div class="flex -mt-12">
                    <div :class="['flex justify-center',{'w-1/2': adventure.created, 'w-full': !adventure.created}]">
                        <v-btn size="large" color="orange-darken-3">New</v-btn>
                    </div>
                    <div class="w-1/2" v-if="adventure.created">
                        <v-btn size="large" color="orange-darken-3" >Continue</v-btn>
                    </div>
                </div>
            </div>
            
			<div class="adventure-info w-full flex flex-col gap-2 relative" :style="`background-image: url(${previewUrl(adventure.id)})`">
				<span class="adventure-name merriweather">{{ adventure.name }}</span>
				<span class="adventure-description roboto">{{ adventure.description }}</span>
			</div>
		</div>
	</div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "AdventuresList",
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
    }
</script>

<style lang="scss" scoped>
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
    .dark {
        --popper-theme-background-color: #333333;
        --popper-theme-background-color-hover: #333333;
        --popper-theme-text-color: white;
        --popper-theme-border-width: 0px;
        --popper-theme-border-radius: 6px;
        --popper-theme-padding: 32px;
        --popper-theme-box-shadow: 0 6px 30px -6px rgba(0, 0, 0, 0.25);
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