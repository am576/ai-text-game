<template>
    <div class="world-elements flex flex-col gap-4">
        <v-card class="w-full p-10">
            <v-card-text class="d-flex justify-between">
                <span class="text-xl">{{name}}</span>
                <v-icon  
                    size="x-large"
                    color="white"
                    icon="mdi-plus" 
                    class="cursor-pointer"
                    @click="addElement"
                >
                </v-icon>
            </v-card-text>
        </v-card>
        <world-element-card v-for="(element, index) in elements" 
            :key="index" 
            :element="element"
            @updateElement="(field, value) => {updateElement(index, field, value)}"
            @remove-element="removeElement(index)" 
        >
        </world-element-card>
        <div class="flex w-full justify-center" v-if="elements.length > 0">
            <v-card class="w-full text-center cursor-pointer" @click="addElement">
                <v-icon 
                size="x-large"
                color="white"
                icon="mdi-plus" 
                >
                </v-icon>
            </v-card>
        </div>
    </div>
</template>

<script>
    import WorldElementCard from './WorldElementCard.vue';
    export default {
        name: "WorldElements",
        components: {
            WorldElementCard
        },
        props: {
            name: {
                type: String,
                required: true
            },
            elements: {
                type: Array,
                required: true,
                default: () => []
            }
        },
        data() {
            return {
            }
        },
        methods: {
            addElement() {
                const newElement = { name: '', description: '' };
                this.$emit('addElement', newElement);
            },
            removeElement(index) {
                this.$emit('removeElement', index);
            },
            updateElement(index, field, value) {
                this.$emit('updateElement', index, field, value);
            },
        }
    }
</script>

<style lang="scss" scoped>

</style>