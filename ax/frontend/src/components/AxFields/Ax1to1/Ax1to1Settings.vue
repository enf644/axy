<template>
  <AxFieldSettings :guid='guid' :options='changedOptions' @closed='$emit("closed")'>
    <br />
    <!-- {{locale("types.Ax1to1.settings-form-header")}}: -->
    <v-autocomplete
      :items='axForms'
      :label='locale("types.Ax1to1.settings-form-select")'
      :rules='formRules'
      @change='setDefaultGrid()'
      chips
      dense
      hide-selected
      item-text='name'
      item-value='dbName'
      v-model='changedOptions.form'
    >
      <template v-slot:selection='{ item, selected }'>
        <v-chip @click:close='clearForm()' close>
          <v-avatar class='grey' left>
            <i :class='`ax-chip-icon fas fa-${item.icon}`'></i>
          </v-avatar>
          {{item.name}}
        </v-chip>
      </template>
    </v-autocomplete>
    <br />
    <!-- {{locale("types.Ax1to1.settings-grid-header")}}: -->
    <v-autocomplete
      :hint='locale("types.Ax1to1.settings-grid-hint")'
      :items='axGrids'
      :label='locale("types.Ax1to1.settings-grid-select")'
      :rules='gridRules'
      chips
      hide-selected
      item-text='name'
      item-value='dbName'
      persistent-hint
      v-model='changedOptions.grid'
    >
      <template v-slot:selection='{ item, selected }'>
        <v-chip @click:close='clearGrid()' close>
          <v-avatar class='grey' left>
            <i :class='`ax-chip-icon fas fa-columns`'></i>
          </v-avatar>
          {{item.name}}
        </v-chip>
      </template>
    </v-autocomplete>
    <br />
    <v-switch
      :label='this.locale("types.Ax1to1.settings-enable-modal")'
      data-cy='settings-enableModal'
      v-model='changedOptions.enableFormModal'
    ></v-switch>
    {{locale("types.Ax1to1.settings-height")}}
    <v-slider max='2000' min='100' thumb-label v-model='changedOptions.height'></v-slider>
  </AxFieldSettings>
</template>

<script>
import AxFieldSettings from '@/components/AxFieldSettings.vue';
import i18n from '@/locale';

export default {
  name: 'Ax1to1Settings',
  components: { AxFieldSettings },
  props: {
    guid: null,
    options: null
  },
  data: () => ({
    changedOptions: {},
    errors: [],
    formRules: [v => !!v || i18n.t('common.field-required')],
    gridRules: [v => !!v || i18n.t('common.field-required')]
  }),
  computed: {
    axForms() {
      return this.$store.getters['home/formsWithoutFolders'];
    },
    axGrids() {
      const selectedForm = this.$store.state.home.forms.find(
        form => form.dbName === this.changedOptions.form
      );
      return selectedForm
        ? selectedForm.grids.edges.map(edge => edge.node)
        : [];
    }
  },
  created() {
    this.$store.dispatch('home/getAllForms', {
      updateTime: Date.now()
    });
    this.changedOptions = this.options;
    if (!this.changedOptions.height) this.changedOptions.height = 400;
    if (!this.changedOptions.enableFormModal) {
      this.changedOptions.enableFormModal = true;
    }
  },
  mounted() {},
  methods: {
    locale(key) {
      return i18n.t(key);
    },
    clearForm() {
      this.changedOptions.form = null;
      this.changedOptions.grid = null;
    },
    clearGrid() {
      this.changedOptions.grid = null;
    },
    setDefaultGrid() {
      const selectedForm = this.$store.state.home.forms.find(
        form => form.dbName === this.changedOptions.form
      );
      if (selectedForm) {
        const defaultGrid = selectedForm.grids.edges.find(
          edge => edge.node.isDefaultView
        );
        if (defaultGrid) this.changedOptions.grid = defaultGrid.node.dbName;
      }
    }
  }
};
</script>

<style scoped>
.editor {
  width: 100%;
  height: 400px;
}
</style>
