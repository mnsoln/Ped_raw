<template>
    <div>
        <Message severity="error">{{ message }}</Message>
        <br />
    </div>
</template>
    
<script>
import Message from 'primevue/message';
export default {
    props: ['message'],
};
</script>