<template>
  <div>
    <div v-html='html'></div>
    <v-alert
      :value='this.html == null'
      type='warning'
    >{{locale("common.no-field-settings-error", {name: this.name})}}</v-alert>
  </div>
</template>

<script>
import i18n from '@/locale';

export default {
  name: 'AxHtml',
  props: {
    name: null,
    dbName: null,
    tag: null,
    options: null,
    value: null
  },
  data: () => ({}),
  computed: {
    html() {
      if (this.options && this.options.code) return this.options.code;
      return null;
    },
    currentName() {
      if (!this.name) return '';
      return this.name;
    }
  },
  methods: {
    locale(key, param) {
      return i18n.t(key, param);
    }
  }
};
</script>

<style scoped>
</style>
