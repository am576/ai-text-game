<template>
   <div class="adventures-list flex justify-between w-2/3 flex-wrap -mx-2">
		<div class="adventure w-1/3 relative flex flex-col px-4 mb-8" 
		v-for="(adventure, index) in adventures" :key="index"
		@mouseover="showControls(index)" @mouseout="hideControls(index)">
			<router-link :to="'/adventure/edit/' + adventure._id" class="link">
				<div v-show="adventure.isHovered" class="edit-btn rounded before:blur-lg absolute top-5 right-10 p-1">
					<font-awesome-icon icon="fa-solid fa-pen-to-square" class=" fa-xl"/>
				</div>
			</router-link>
			<h3 class="text-3xl text-center absolute top-5 w-full"></h3>
			<img :src="previewUrl(adventure._id)" style="object-fit: contain;" class="self-start">
            <div v-show="adventure.isHovered">
                <div class="flex -mt-12">
                    <div :class="['flex justify-center',{'w-1/2': adventure.created, 'w-full': adventure.created === 'false'}]">
						<v-btn size="large" color="orange-darken-3" @click="startAdventure(adventure._id)">New</v-btn>
                    </div>
                    <div class="w-1/2" v-if="adventure.created === 'true'">
                        <v-btn size="large" color="orange-darken-3" @click="loadAdventure(adventure._id)">Continue</v-btn>
                    </div>
                </div>
            </div>
            
			<div class="adventure-info w-full flex flex-col gap-2 relative" :style="`background-image: url(${previewUrl(adventure._id)})`">
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
			showControls(index) {
				this.adventures[index].isHovered = true
			},
			hideControls(index) {
				this.adventures[index].isHovered = false
			},
			startAdventure(adventure_id) {
				axios.post(`${process.env.VUE_APP_BACKEND_URL}/start_game`, {adventure_id: adventure_id})
				.then(() => {
					this.$router.push({ name: 'adventure', params: { id: adventure_id } })	
				})
			},
			loadAdventure(adventure_id) {
				axios.post(`${process.env.VUE_APP_BACKEND_URL}/load_game`, {adventure_id: adventure_id})
				.then(() => {
					this.$router.push({ name: 'adventure', params: { id: adventure_id } })	
				})
			}


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
.edit-btn {
	background-color: rgba(83, 83, 83, 0.54);
	
}
</style>