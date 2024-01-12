<template>
    <div>
    <v-hover>
        <template v-slot:default="{ isHovering, props}">
            <div class="world-element-card" v-bind="props">
                <v-card>
                    <v-card-text>
                        
                        <v-text-field placeholder="Name" variant="solo-filled" ref="nameInput"></v-text-field>
                        <v-textarea spellcheck="false" variant="outlined" hint="Give a 3-5 sentence description" cols="30" rows="5"></v-textarea>
                        <div class="flex justify-end" v-show="isHovering">
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
            }  
        },
        methods: {
            removeElement() {
                this.$emit('remove-element');
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
</style>