import components from './components';
import utils from './utils';

export function install(Vue) {
  Object.keys(components).forEach((name) => {
    Vue.component(name, components[name]);
  });

  // Extend trame.utils
  Object.assign(window.trame.utils, utils);
}
