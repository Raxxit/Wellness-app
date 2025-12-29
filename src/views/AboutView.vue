<script setup>
    
    import { onMounted } from 'vue/dist/vue.js';
    import { WOW } from 'wowjs';


    import aboutImage from '@/assets/img/1.jpg';

    onMounted(()=> {
        new WOW().init();
    })


</script>