<template>
    <div class="homepage bg-slate-800 h-screen flex justify-center">
        
        <div class="w-1/3 flex">
            <div class="w-full flex flex-col justify-start items-center p-10" v-show="worldPreview">
                <h3 class="text-3xl  font-bold text-slate-200 text-center">World preview</h3>
                <img :src="worldPreview" style="object-fit: contain;" class="self-start"/>
            </div>
        </div>
        <div class="w-1/3 flex flex-col gap-8">
            <div v-if="errors.network">{{ errors.network.message }}</div>
            <div class="flex items-center justify-start">
                <router-link to="/" class="link">
                    <font-awesome-icon icon="fa-solid fa-angle-left" class="text-sky-500 hover:text-sky-700  mr-auto" size="2xl"/>
                </router-link>
                <h1 class="mx-auto text-5xl py-10 font-bold text-slate-200 text-center">{{ pageTitle }} your adventure</h1>
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
            <div class="w-full flex flex-col gap-4">
                <h3 class="text-3xl font-bold text-slate-200">Character</h3>
                
                <div>
                    <h3 class="text-2xl font-bold text-slate-200">Age</h3>
                    <v-btn-toggle
                        v-model="adventure.character.age"
                        divided
                        color="purple-darken-4"
                    >
                        <v-btn v-for="(age, index) in ages" :key="index" :value="age">{{ age }}</v-btn>
                    </v-btn-toggle>
                </div>
                <div>
                    <h3 class="text-2xl font-bold text-slate-200">Gender</h3>
                    <v-btn-toggle
                        v-model="adventure.character.gender"
                        divided
                        color="purple-darken-4"
                    >
                        <v-btn v-for="(gender, index) in genders" :key="index" :value="gender">{{ gender }}</v-btn>
                    </v-btn-toggle>
                </div>
                <div>
                    <label for="character_description" class="text-2xl font-bold text-slate-200">Character backstory</label>
                    <Popper placement="right" class="dark">
                        <template #content>
                        <div>Describe your character - who are you? What are you up to? What is your story?</div>
                        </template>
                        <textarea id="charscter_description" v-model="adventure.character.description" class="user-input"></textarea>
                    </Popper>
                    <span v-if="errors.character_description" class="error">{{ errors.character_description }}</span>
                    <v-btn @click="generateAvatarPreview">Create avatar</v-btn>
                </div>
                
            </div>
            <div class="w-full" v-show="adventure.avatarDescription && !generatingAvatarPrompt">
                <label for="avatar_description" class="text-3xl font-bold text-slate-200">Avatar</label>
                <Popper placement="right" class="dark">
                    <template #content>
                      <div>This is the initial avatar of your character. It will change in the course of the story.</div>
                    </template>
                    <input type="text" id="avatar_description" v-model="adventure.avatarDescription" @input="generateAvatar" class="user-input">
                </Popper>
                
                <span v-if="errors.avatar_description" class="error">{{ errors.avatar_description }}</span>
            </div>
            <div v-show="!generatingAvatar" class="flex gap-3 items-center justify-center">
                <button @click.prevent="submitAdventure" :disabled="isSaving" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                {{ btnCaption }}
            </button>
            <clip-loader :loading="isSaving" :color="'#3b82f6'" :size="'25px'"></clip-loader>
            </div>
        </div>
        <div class="w-1/3 flex justify-center"> 
            <div class="w-full flex flex-col justify-start items-center p-10" v-show="avatarPreview">
                <div class="flex items-center justify-center gap-4">
                    <h3 class="text-3xl font-bold text-slate-200">Avatar preview</h3>
                    <font-awesome-icon v-show="!generatingAvatar" icon="fa-solid fa-rotate-right" class="text-sky-500 hover:text-sky-700  mr-auto cursor-pointer" size="2xl" @click="generateAvatar"/>
                </div>
                <div :class="['avatar-preview',{ 'with-before': generatingAvatar }]">
                    <img :src="avatarPreview" style="object-fit: contain;" class="self-start" alt="Avatar preview" />
                    <clip-loader :loading="generatingAvatar" :color="'#ffffff'" :size="'50px'"></clip-loader>
                </div>
                
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
                adventure_id: '',
                adventure: {
                    name: "Invasion",
                    worldDescription: "A big Russian city destroyed by alien invasion",
                    avatarDescription: " A determined and resilient man in his late twenties or early thirties, haunted by the loss of his wife during the alien invasion, gazes intensely at the viewer with steely resolve.",
                    character: {
                        age: "18-25",
                        gender: "Male",
                        description: "You are a former programmer who survived the alien invasion. Your wife was killed in the first hours of attack. You have nothing left but revenge and survival"
                    },
                },
                
                worldPreview: '',
                avatarPreview: '',
                errors: {},
                isSaving : false,
                genders: ['Male', 'Female'],
                ages: ['18-25', '25-35', '35-45', '45-55', '55-60', '60-70', '70+'],
                current_message: '',
                generatingAvatar: false,
                generatingAvatarPrompt: false,
                defaultAvatar: ''
            };
        },
        methods: {
            submitAdventure() {
                this.isSaving = true
                this.errors = {};
                const formData = new FormData()
                if(this.adventure_id) {
                    formData.append('adventure_id', this.adventure_id)
                }
                formData.append('adventure', JSON.stringify(this.adventure));
                
                const url = process.env.VUE_APP_BACKEND_URL;
                axios.post(`${url}/save_adventure`, formData,
                {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }
                )
                .then(() => {
                    
                    router.push('/')
                    this.isSaving = false
                })
                .catch(error => {
                    if (error.stack) {
                        this.errors.network = {message: "Something went wrong. Please try again later."}
                    }    
                    if (error.response) {
                        this.errors = error.response.data;
                    } else if (error.request) {
                        console.log(error.request);
                    } else {
                        console.log(error.message);
                    }
                })
                .finally(() => {
                    this.isSaving = false
                })
            },
            generateAvatar: debounce(function() {
                this.generatingAvatar = true;
                const url = process.env.VUE_APP_BACKEND_URL;
                axios.post(`${url}/avatar_preview`, {prompt: this.adventure.avatarDescription},
                {
                    headers: {
                    'Content-Type': 'application/json'
                    },responseType: 'blob'
                }, )
                    .then(response => {
                        const blob = new Blob([response.data], { type: 'image/png' });
                        this.avatarPreview = URL.createObjectURL(blob);
                        this.generatingAvatarPrompt = false
                    })
                    .catch(error => {
                    console.log('Error:', error);
                    })
                    .finally(() => {
                    this.generatingAvatar = false
                    })
            }, 500),
            async generateAvatarPrompt() {
                this.generatingAvatarPrompt = true
                const prompt = `Here is a description of a adventure.character:\n"${this.adventure.character.description}. ${this.adventure.character.gender}. ${this.adventure.character.age} years old"\n
                    Describe it with 1-2 sentences, how you would it to an artist to paint a picture of this character. It must be a close up portrait. Don't mention character's profession.`
                const body = {
                    model: "dolphin",
                    prompt: prompt
                };
                const response = await fetch("http://127.0.0.1:11434/api/generate", {
                    method: "POST",
                    body: JSON.stringify(body)
                });

                const reader = response.body?.getReader();
                if (!reader) {
                    throw new Error("Failed to read response body");
                }

                let content = "";
                let done = false;
                let avatar_prompt = ""
                while (!done) {
                    const { done: isDone, value } = await reader.read();
                    done = isDone;
                    if (!done) {
                        const rawjson = new TextDecoder().decode(value);
                        const json = JSON.parse(rawjson);
                        content += json.response;
                        avatar_prompt = content
                    }
                }
                this.adventure.avatarDescription = avatar_prompt
                this.generatingAvatarPrompt = false
            },
            async generateAvatarPreview() {
                this.generatingAvatar = true
                this.avatarPreview = this.defaultAvatar
                await this.generateAvatarPrompt()
                this.generateAvatar()
            },
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
            loadAdventure(id) {
                axios.get(`${process.env.VUE_APP_BACKEND_URL}/get_adventure?id=${id}`)
                .then(response => {
                    const adventure = response.data
                    this.adventure.name = adventure.name
                    this.adventure.worldDescription = adventure.description
                    this.adventure.character.description = adventure.character_description
                    this.adventure.avatarDescription = adventure.avatar_description
                    this.worldPreview = this.preview(id)
                    this.avatarPreview = this.avatar(id)
                })
            },
            preview(adventure_id) {
				return require(`../assets/adventures/${adventure_id}/preview.png`);
			},
            avatar(adventure_id) {
				return require(`../assets/adventures/${adventure_id}/avatar.png`);
			},
            
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
                if (this.isSaving) {
                    return "Saving..."
                }
                else {
                    if (this.$route.params.id) {
                        return "Save adventure"
                    }
                    else {
                        return "Create adventure"
                    }
                }
            },
            avatarPrePrompt() {
                return "3d sci-fi concept art, portrait of a adventure.character. " + this.adventure.character.gender + " " + this.character.age + " years old. \n"
            },
            pageTitle() {
                if (this.$route.params.id) {
                    return "Change"
                }
                else {
                    return "Create"
                }
            }
        },
        created() {
            this.defaultAvatar = new URL('/src/assets/default_avatar.png', import.meta.url).href
            if (this.$route.params.id) {
                this.adventure_id = this.$route.params.id
                this.loadAdventure(this.$route.params.id)
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
    .avatar-preview {
        position: relative;
        .v-spinner {
            position: absolute;
            left: 45%;
            top: 45%;
        }
        &.with-before::before {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            backdrop-filter: blur(30px);
            background-color: rgba(0, 0, 0, 0.54);
        }
    }
    .avatar-preview::before {
        content: "";
        
    }
    

</style>