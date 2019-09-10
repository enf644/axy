// Core dependencies

// import 'typeface-roboto';
// import 'roboto-npm-webfont';
import Vue from 'vue';
import vueCustomElement from 'vue-custom-element'; // create web component from vue component
import 'document-register-element'; // polyfill for vue-custom-element
import 'animate.css/animate.min.css';
import logger from './logger';
import './assets/ax-core.css'; // TODO check if ./ needed
import VModal from 'vue-js-modal';

// Admin dependencies
import VueResize from 'vue-resize'; // detect element resize
// import '@fortawesome/fontawesome-free/js/all.js';
import '@fortawesome/fontawesome-free/css/all.css';
import AsyncComputed from 'vue-async-computed';

import 'vue-resize/dist/vue-resize.css';
// import vuetify from '@/plugins/vuetify';
import Vuetify, {
  VTextField,
  VSnackbar,
  VDialog,
  VCard,
  VToolbar,
  VIcon,
  VToolbarTitle,
  VCardText,
  VCardTitle,
  VCardActions,
  VSpacer,
  VBtn
} from 'vuetify/lib';
// import 'vuetify/dist/vuetify.min.css';

// import 'vuetify/src/stylus/app.styl';
import VuetifyDialog from 'vuetify-dialog';
import 'vuetify-dialog/dist/vuetify-dialog.css';

import App from './App.vue';
import router from './router';
import store from './store';
import i18n from './locale.js';
import AxTest from './components/AxTest.vue';

// Dev dependencies
// import VueDummy from 'vue-dummy'; // create lorum ipsum

// Getting hostname of server from src of included script
// no matter how many scripts a page contains,
// the one currently starting to execute is the last one;

Vue.use(VModal, { dynamic: true, injectModalsContainer: true });
Vue.use(Vuetify, {
  components: {
    VTextField,
    VSnackbar,
    VDialog,
    VCard,
    VCardTitle,
    VToolbar,
    VIcon,
    VToolbarTitle,
    VCardText,
    VCardActions,
    VSpacer,
    VBtn
  }
});
Vue.use(vueCustomElement);
Vue.use(VueResize);
// Vue.use(VueDummy);
Vue.use(AsyncComputed);
Vue.config.productionTip = false;

const gridPromise = () => import(/* webpackChunkName: "ax-grid" */ './components/AxGrid.vue').then(m => m.default);
Vue.customElement(
  'ax-grid',
  gridPromise,
  {
    props: ['form', 'grid', 'update_time', 'arguments', 'width', 'height']
  }
);

const formPromise = () => import(/* webpackChunkName: "ax-form" */ './components/AxForm.vue').then(m => m.default);
Vue.customElement('ax-form', formPromise, { props: ['db_name', 'row_guid', 'update_time', 'opened_tab'] });

Vue.customElement('ax-test', AxTest);


const vuetify = new Vuetify({
  icons: {
    iconfont: 'fa'
  }
});
Vue.config.productionTip = false;

Vue.use(VuetifyDialog, {
  context: {
    vuetify
  },
  toast: { position: 'bottom-right' }
});

Vue.prototype.$log = logger; // Custom logger


new Vue({
  router,
  store,
  vuetify,
  i18n,
  render: h => h(App)
}).$mount('#ax-app');
