<template>
    <div class="world-elements flex flex-col gap-4">
        <v-card class="w-full p-10">
            <v-card-text class="d-flex justify-between">
                <span class="text-xl">{{name}}</span>
                <v-icon  
                    size="x-large"
                    color="green-lighten-2"
                    icon="mdi-plus" 
                    class="cursor-pointer"
                    @click="addElement"
                >
                </v-icon>
            </v-card-text>
        </v-card>
        <world-element-card v-for="(element, index) in elements" :key="index">{{ element.text }}</world-element-card>
        <div class="flex w-full justify-center" v-if="elements.length > 0">
            <v-card class="w-full text-center cursor-pointer" @click="addElement">
                <v-icon 
                size="x-large"
                color="green-lighten-2"
                icon="mdi-plus" 
            >
                </v-icon>
            </v-card>
            
        </div>
    </div>
      
</template>

<script>
    export default {
        name: "WorldElements",
        props: {
            name: {
                type: String,
                required: true
        }
        },
        data() {
            return {
                elements: []
            }
        },
        methods: {
            addElement() {
                this.elements.push({ text: "" })
            }
        }
    }
</script>

<style lang="scss" scoped>

</style>