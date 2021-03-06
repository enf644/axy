<template>
  <div class='card'>
    <v-btn :ripple='false' @click='closeModal' class='close' color='black' icon text>
      <i class='fas fa-times close-ico'></i>
    </v-btn>

    <h3>{{$t("grids.query-builder-header")}}</h3>

    <div id='monacoDock'>
      <div id='monacoWrapper'>
        <monaco-editor
          :options='monacoOptions'
          @editorDidMount='initMonaco'
          class='editor'
          data-cy='code-editor'
          language='python'
          ref='editor'
          theme='vs-dark'
          v-model='code'
        ></monaco-editor>
      </div>
    </div>

    <br />
    <div class='actions'>
      <v-btn @click='updateGridCode' small>
        <i class='fas fa-filter'></i>
        &nbsp; {{$t("common.save")}}
      </v-btn>
      <v-btn @click='closeModal' small>
        <i class='fas fa-times'></i>
        &nbsp; {{$t("common.confirm-no")}}
      </v-btn>
    </div>
  </div>
</template>

<script>
import apolloClient from '@/apollo';
import gql from 'graphql-tag';
import MonacoEditor from 'vue-monaco';
import * as monaco from 'monaco-editor';

export default {
  name: 'TheQueryModal',
  components: { MonacoEditor },
  data: () => ({
    code: '',
    monacoOptions: null,
    fullScreenMode: false
  }),
  // components: { MonacoEditor },
  computed: {
    gridGuid() {
      return this.$store.state.grids.guid;
    }
  },
  mounted() {
    this.code = this.$store.state.grids.code;
  },
  methods: {
    initMonaco(editor) {
      editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KEY_S, () => {
        this.updateGridCode(false);
      });
      editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
        if (!this.fullScreenMode) {
          this.fullScreenMode = true;
          document.body.appendChild(document.getElementById('monacoWrapper'));
          setTimeout(() => {
            editor.layout();
          }, 100);
        } else {
          this.fullScreenMode = false;
          const dock = document.getElementById('monacoDock');
          dock.appendChild(document.getElementById('monacoWrapper'));
          setTimeout(() => {
            editor.layout();
          }, 100);
        }
      });
    },
    closeModal() {
      this.$emit('close');
    },
    updateGridCode() {
      this.$store.commit('grids/setCode', this.code);

      const UPDATE_CODE = gql`
        mutation($guid: String!, $code: String) {
          updateGridCode(guid: $guid, code: $code) {
            ok
          }
        }
      `;
      apolloClient
        .mutate({
          mutation: UPDATE_CODE,
          variables: {
            guid: this.gridGuid,
            code: this.code
          }
        })
        .then(data => {
          // const newForm = data.data.getForm.form;
          const msg = this.$t('grids.grid-updated');
          this.$store.commit('grids/setUpdateTime', Date.now());
          this.$dialog.message.success(
            `<i class="fas fa-columns"></i> &nbsp ${msg}`
          );
          this.closeModal();
        })
        .catch(error => {
          const msg = `Error in updateGridCode apollo client => ${error}`;
          this.$store.commit('home/setShowErrorMsg', msg);
        });

      // this.$store.dispatch('grids/updateGrid', {}).then(() => {
      //   const msg = this.$t('grids.grid-updated');
      //   this.$store.commit('grids/setUpdateTime', Date.now());
      //   this.$dialog.message.success(
      //     `<i class="fas fa-columns"></i> &nbsp ${msg}`
      //   );
      //   this.closeModal();
      // });
    }
  }
};
</script>

<style scoped>
.card {
  padding: 25px;
}
.close {
  position: absolute;
  right: 10px;
  top: 10px;
}
.close-ico {
  font-size: 20px;
}
.actions {
  justify-content: space-between;
  display: flex;
}
.editor {
  width: 100%;
  height: 400px;
}
</style>
