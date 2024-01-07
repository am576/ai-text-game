<template>
    <div class="homepage bg-slate-800 h-screen flex justify-center">
        <div class="w-1/3 flex">
            <div class="w-full flex flex-col justify-start items-center p-10" v-show="worldPreview">
                <h3 class="text-3xl  font-bold text-slate-200 text-center">World preview</h3>
                <img :src="worldPreview" style="object-fit: contain;" class="self-start"/>
            </div>
        </div>
        <div class="w-1/3 flex flex-col gap-8">
            <div class="flex items-center justify-start">
                <router-link to="/" class="link">
                    <font-awesome-icon icon="fa-solid fa-angle-left" class=" text-sky-500 hover:text-sky-700  mr-auto" size="2xl" />
                </router-link>
                <h1 class="mx-auto text-5xl py-10 font-bold text-slate-200 text-center">Create your adventure</h1>
            </div>
            <div class="w-full">
                <input type="text" id="name" v-model="adventure.name" class="user-input" placeholder="Give your adventure a name">
                <span v-if="errors.name" class="error">{{ errors.name }}</span>
            </div>
            <div class="w-full">
                <label for="description" class="text-3xl font-bold text-slate-200">World</label>
                <Popper placement="right" class="dark">
                    <template #content>
                      <div>Give a short description of your world</div>
                    </template>
                    <textarea id="description" v-model="adventure.worldDescription" @input="generateWorldPreview" class="user-input"
                    placeholder="A world where an alien invasion took place. An alien race attacked the Earth. "></textarea>
                </Popper>
                <span v-if="errors.description" class="error">{{ errors.description }}</span>
            </div>
            <div class="w-full">
                <label for="character_description" class="text-3xl font-bold text-slate-200">Character</label>
                <Popper placement="right" class="dark">
                    <template #content>
                      <div>Describe your character - who are you? What are you up to? What is your story?</div>
                    </template>
                    <textarea id="charscter_description" v-model="adventure.characterDescription" class="user-input"></textarea>
                </Popper>
                <span v-if="errors.character_description" class="error">{{ errors.character_description }}</span>
            </div>
            <div class="w-full">
                <label for="avatar_description" class="text-3xl font-bold text-slate-200">Avatar</label>
                <Popper placement="right" class="dark">
                    <template #content>
                      <div>This is the initial avatar of your character. It will change in the course of the story.</div>
                    </template>
                    <input type="text" id="avatar_description" v-model="adventure.avatarDescription" @input="generateAvatar" class="user-input">
                </Popper>
                <span v-if="errors.avatar_description" class="error">{{ errors.avatar_description }}</span>
            </div>
            <div class="flex gap-3 items-center justify-center">
                <button @click.prevent="submitAdventure" :disabled="isSaving" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                {{ btnCaption }}
            </button>
            <clip-loader :loading="isSaving" :color="spinner.color" :size="spinner.size"></clip-loader>
            </div>
            
        </div>
        <div class="w-1/3 flex justify-center">
            <div class="w-full flex flex-col justify-start p-10" v-show="avatarPreview">
                <h3 class="text-3xl  font-bold text-slate-200 text-center">Avatar preview</h3>
                <img :src="avatarPreview" style="object-fit: contain;" class="self-start" alt="Avatar preview" />
            </div>
        </div>
    </div>
  </template>

<script>
    import axios from 'axios';
    import router from '@/router'
    import { debounce } from 'lodash';
    import Popper from "vue3-popper";
    import ClipLoader from 'vue-spinner/src/ClipLoader.vue'

    export default {
        name: "AdventureCreator",
        components: {
            Popper,
            ClipLoader
        },
        data() {
            return {
                adventure: {},
                worldPreview: '',
                avatarPreview: '',
                errors: {},
                isSaving : false,
                spinner: {
                    size: '50px',
                    color: '#3b82f6',
                }
            };
        },
        methods: {
            submitAdventure() {
                this.isSaving = true
                this.errors = {};
                const formData = new FormData()
                for (const [key, value] of Object.entries(this.adventure)) {
                   formData.append(key, value);
                }
                const url = process.env.VUE_APP_BACKEND_URL;
                axios.post(`${url}/save_adventure`, formData,
                {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }
                )
                .then(() => {
                    this.isSaving = false
                    router.push('/')
                })
                .catch(error => {
                    if (error.response) {
                        this.errors = error.response.data;
                    } else if (error.request) {
                        console.log(error.request);
                    } else {
                        console.log(error.message);
                    }
                });
            },
            generateAvatar: debounce(function() {
                const url = process.env.VUE_APP_BACKEND_URL;
                axios
                axios.post(`${url}/avatar_preview`, {prompt: this.adventure.avatarDescription},
                {
                    headers: {
                    'Content-Type': 'application/json'
                    },responseType: 'blob'
                }, )
                    .then(response => {
                        const blob = new Blob([response.data], { type: 'image/png' });
                        this.avatarPreview = URL.createObjectURL(blob);
                    })
                    .catch(error => {
                    console.log('Error:', error);
                    });
            }, 500),
            generateWorldPreview: debounce(function() {
                const url = process.env.VUE_APP_BACKEND_URL;
                axios
                axios.post(`${url}/world_preview`, {prompt: this.adventure.worldDescription},
                {
                    headers: {
                    'Content-Type': 'application/json'
                    },responseType: 'blob'
                }, )
                    .then(response => {
                    const blob = new Blob([response.data], { type: 'image/png' });
                    this.worldPreview = URL.createObjectURL(blob);
                    })
                    .catch(error => {
                    console.log('Error:', error);
                    });
            }, 500),
        },
        computed: {
            previewUrl() {
                if (this.imageUrl) {
                    return this.imageUrl;
                } else {
                    return '';
                }
            },
            btnCaption() {
                return this.isSaving ? "Saving..." : "Create adventure";
            }
        }
    }
    
</script>

<style lang="scss" scoped>
    .inline-block {
        width: 100% !important;
        margin: 0 !important;
        border: 0 !important;
    }
    img {
        width: 512px;
        height: 512px;
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
    

</style>