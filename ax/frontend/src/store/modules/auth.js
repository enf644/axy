import apolloClient from '../../apollo';
import gql from 'graphql-tag';
import logger from '../../logger';
import { getAxHostProtocol } from '@/misc';
import Cookies from 'js-cookie'

const getDefaultState = () => {
  // TODO window can be null when web-component used
  return {
    accessToken: Cookies.get('access_token'),
    refreshToken: Cookies.get('refresh_token')
  }
}

const LOGOUT = gql`
  mutation {
    logoutUser {
      ok    
    }
  }
`;

const getters = {};

const actions = {
  logOut(context, toAdmin) {
    const host = getAxHostProtocol();
    if (toAdmin) window.location.href = `${host}/api/signout?to_admin=1`;
    else window.location.href = `${host}/api/signout`;
  },
  goToPages(context) {
    const host = getAxHostProtocol();
    // console.log('auth -> goToPages');
    window.location.href = `${host}/pages/`;
  }
};

const mutations = {
  resetState(state) {
    Object.assign(state, getDefaultState())
  },
  setTokens(state, payload) {
    state.accessToken = payload.access;
    state.refreshToken = payload.refresh;
  }
};


const state = getDefaultState();

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
