<template>
    <div class="homepage bg-slate-800 h-screen flex flex-col items-center">
        <h1 class="text-5xl py-10 font-bold text-slate-200 text-center">Create your adventure</h1>
        <div>
            <label for="name">Name:</label>
            <input type="text" id="name" v-model="adventureName">
            <span v-if="errors.name" class="error">{{ errors.name }}</span>
        </div>
        <div>
            <label for="description">Description:</label>
            <textarea id="description" v-model="adventureDescription" @input="handleInput"></textarea>
            <span v-if="errors.description" class="error">{{ errors.description }}</span>
        </div>
        <button @click.prevent="submitAdventure">Submit</button>
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" @click="testComfy">
            Test
        </button>
        <img :src="imageUrl">
    </div>
  </template>

<script>
    import axios from 'axios';
    import { debounce } from 'lodash';

    export default {
        name: "AdventureCreator",
        data() {
            return {
                imageUrl : '',
                adventureType: '',
                adventureName: '',
                adventureDescription: '',
                errors: {},
            };
        },
        methods: {
            submitAdventure() {
                this.errors = {};

                axios.post('/api/addAdventure', {
                    type: this.adventureType,
                    name: this.adventureName,
                    description: this.adventureDescription
                },{ responseType: 'arraybuffer' })
                .then(response => {
                    // Handle successful response
                    console.log(response.data);
                })
                .catch(error => {
                    // Handle error response
                    if (error.response) {
                        this.errors = error.response.data;
                    } else if (error.request) {
                        console.log(error.request);
                    } else {
                        console.log(error.message);
                    }
                });
            },
            handleInput: debounce(function() {
                const url = process.env.VUE_APP_BACKEND_URL;
                axios
                axios.post(`${url}/generate_preview`, {prompt: this.adventureDescription},
                {
                    headers: {
                    'Content-Type': 'application/json'
                    },responseType: 'blob'
                }, )
                    .then(response => {
                    const blob = new Blob([response.data], { type: 'image/png' });
                    this.imageUrl = URL.createObjectURL(blob);
                    })
                    .catch(error => {
                    console.log('Error:', error);
                    });
                }, 500),
            testComfy() {
                const url = process.env.VUE_APP_BACKEND_URL
                axios.post(`${url}/generate_preview`, {prompt: "test prompt"},
                {
                    headers: {
                    'Content-Type': 'application/json'
                    },responseType: 'blob'
                }, )
                .then(response => {
                    const blob = new Blob([response.data], { type: 'image/png' });
                    this.imageUrl = URL.createObjectURL(blob);
                    console.log(this.imageUrl)
                })
                .catch(error => {
                    if (error.response) {
                        console.log(error.response.data);
                        console.log(error.response.status);
                        console.log(error.response.headers);
                    } 
                    else if (error.request) {
                        console.log(error.request);
                    } 
                    else {
                    // Something happened in setting up the request that triggered an Error
                        console.log('Error', error.message);
                    }
                });
            },
        },
        computed: {
            previewUrl() {
                if (this.imageUrl) {
                    return this.imageUrl;
                } else {
                    return '';
                }
            }
        }
    }
    
</script>

<style lang="scss" scoped>

</style>