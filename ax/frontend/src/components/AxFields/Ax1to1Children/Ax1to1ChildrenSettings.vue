<template>
  <AxFieldSettings :guid='guid' :options='changedOptions' @closed='$emit("closed")'>
    <v-container>
      <v-row>
        <v-col class='mr-3'>
          <v-autocomplete
            :items='axForms'
            :label='locale("types.Ax1to1Children.settings-form-select")'
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
        </v-col>
        <v-col class='ml-3'>
          <v-autocomplete
            :hint='locale("types.Ax1tomTable.settings-inline-grid-hint")'
            :items='axGrids'
            :label='locale("types.Ax1tomTable.settings-inline-grid-select")'
            :rules='gridRules'
            chips
            hide-selected
            item-text='name'
            item-value='dbName'
            persistent-hint
            v-model='changedOptions.inline_grid'
          >
            <template v-slot:selection='{ item, selected }'>
              <v-chip @click:close='clearInlineGrid()' close>
                <v-avatar class='grey' left>
                  <i :class='`ax-chip-icon fas fa-columns`'></i>
                </v-avatar>
                {{item.name}}
              </v-chip>
            </template>
          </v-autocomplete>
        </v-col>
      </v-row>
      <v-row>
        <v-col class='mr-3'>
          <v-autocomplete
            :hint='locale("types.Ax1to1Children.settings-field-hint")'
            :items='axFields'
            :label='locale("types.Ax1to1Children.settings-field-select")'
            :rules='fieldRules'
            chips
            hide-selected
            item-text='name'
            item-value='guid'
            persistent-hint
            v-model='changedOptions.field'
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
        </v-col>
        <v-col class='ml-3'>
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
        </v-col>
      </v-row>
      <v-row>
        <v-col class='mr-3'>
          {{locale("types.Ax1tomTable.settings-inline-height")}}
          <v-slider max='1000' min='300' thumb-label v-model='changedOptions.inline_height'></v-slider>
        </v-col>
        <v-col class='ml-3'>
          {{locale("types.Ax1to1.settings-height")}}
          <v-slider max='2000' min='300' thumb-label v-model='changedOptions.height'></v-slider>
        </v-col>
      </v-row>
    </v-container>
  </AxFieldSettings>
</template>

<script>
import AxFieldSettings from '@/components/AxFieldSettings.vue';
import i18n from '@/locale.js';
import apolloClient from '@/apollo';
import gql from 'graphql-tag';

export default {
  name: 'Ax1tomSettings',
  components: { AxFieldSettings },
  props: {
    guid: null,
    options: null
  },
  data: () => ({
    changedOptions: {},
    changedPrivateOptions: {},
    errors: [],
    axFields: [],
    formRules: [v => !!v || i18n.t('common.field-required')],
    gridRules: [v => !!v || i18n.t('common.field-required')],
    fieldRules: [v => !!v || i18n.t('common.field-required')]
  }),
  computed: {
    axForms() {
      return this.$store.state.home.forms;
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
    if (!this.changedOptions.isWholeRow) this.changedOptions.isWholeRow = true;
    if (!this.changedOptions.height) this.changedOptions.height = 400;
    if (!this.changedOptions.inline_height) {
      this.changedOptions.inline_height = 400;
    }
    if (!this.changedOptions.enableFormModal) {
      this.changedOptions.enableFormModal = true;
    }

    if (this.changedOptions.form) {
      const selectedForm = this.$store.state.home.forms.find(
        form => form.dbName === this.changedOptions.form
      );
      if (selectedForm) {
        this.getFields(selectedForm);
      }
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
      this.changedOptions.field = null;
      this.axFields = [];
    },
    clearInlineGrid() {
      this.changedOptions.inline_grid = null;
    },
    clearGrid() {
      this.changedOptions.grid = null;
    },
    setDefaultGrid() {
      const selectedForm = this.$store.state.home.forms.find(
        form => form.dbName === this.changedOptions.form
      );
      if (selectedForm) {
        this.getFields(selectedForm);
        const defaultGrid = selectedForm.grids.edges.find(
          edge => edge.node.isDefaultView
        );
        if (defaultGrid) {
          this.changedOptions.grid = defaultGrid.node.dbName;
          this.changedOptions.inline_grid = defaultGrid.node.dbName;
        }
      }
    },
    getFields(selectedForm) {
      const TO1_FIELDS = gql`
        query(
          $childFormGuid: String!
          $fieldGuid: String!
          $updateTime: String
        ) {
          to1Fields(
            childFormGuid: $childFormGuid
            fieldGuid: $fieldGuid
            updateTime: $updateTime
          ) {
            guid
            name
            dbName
          }
        }
      `;
      const vars = {
        childFormGuid: selectedForm.guid,
        fieldGuid: this.guid,
        updateTime: Date.now()
      };
      apolloClient
        .query({
          query: TO1_FIELDS,
          variables: vars
        })
        .then(data => {
          this.axFields = data.data.to1Fields;
          if (this.axFields && this.axFields.length > 0)
            this.changedOptions.field = this.axFields[0].guid;
        })
        .catch(error => {
          this.$log.error(`Error in getFields gql => ${error}`);
          this.$dialog.message.error(error);
        });
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
