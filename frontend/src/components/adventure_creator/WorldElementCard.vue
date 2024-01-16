<template>
    <div>
    <v-hover>
        <template v-slot:default="{ isHovering, props}">
            <div class="world-element-card" v-bind="props">
                <v-card>
                    <v-card-text>
                        
                        <v-text-field 
                            placeholder="Name" 
                            variant="solo-filled" 
                            ref="nameInput" 
                            v-model="name"
                            @input="updateElement('name', $event.target.value)"
                        >
                        </v-text-field>
                        <v-textarea 
                            spellcheck="false" 
                            variant="outlined" 
                            hint="Give a 3-5 sentence description" 
                            cols="30" rows="5" 
                            v-model="description"
                            @input="updateElement('description', $event.target.value)"
                        >
                        </v-textarea>
                        <div class="flex justify-between" v-show="isHovering">
                            <v-icon 
                                size="x-large"
                                color="blue"
                                icon="mdi-brain"
                                class="generate cursor-pointer"
                                @click="generateElementDescription" 
                            />    
                            <v-icon 
                                size="x-large"
                                color="light-green-lighten-2"
                                icon="mdi-trash-can-outline"
                                class="remove-item cursor-pointer"
                                @click="removeElement" 
                            />    
                        </div>
                        <!-- <textarea name="" id="" class="w-full text-lg" spellcheck="false" cols="30" rows="5">Hello</textarea> -->
                    </v-card-text>
                </v-card>
            </div>
        </template>
    </v-hover>
    </div>
</template>

<script>
    export default {
        name: "WorldElementCard",
        props: {
            isHovering: {
                type: Boolean,
                default: false
            },
            element: {
                type: Object,
                default: () => ({
                    name : "",
                    description: ""
                }),
                required: true
            }  
        },
        data() {
            return {
                
            }
        },
        methods: {
            generateElementDescription() {
                this.element_description = "AI-generated text"
            },
            updateElement(property, value) {
              this.$emit('updateElement', property, value);
            },
            removeElement() {
                this.$emit('remove-element');
            }
        },
        computed: {
            name: {
                get() {
                    return this.element.name;
                },
                set(newValue) {
                    this.$emit('input', { ...this.element, name: newValue });
                }
                },
            description: {
                get() {
                    return this.element.description;
                },
                set(newValue) {
                    this.$emit('input', { ...this.element, description: newValue });
                }
            }
        },
        created() {
            this.$nextTick(()=>{
                this.$refs["nameInput"].focus()
            });
        }
    }
</script>

<style lang="scss" scoped>
.remove-item {
    position: absolute;
    bottom: 5px;
    right: 20px;
}
.generate {
    position: absolute;
    bottom: 5px;
    left: 47%;
}
</style>