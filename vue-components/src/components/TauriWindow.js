import {
  LogicalPosition,
  LogicalSize,
  WebviewWindow,
  appWindow,
} from "@tauri-apps/api/window";
import { ref, onBeforeUnmount, watch } from "vue";

const OPTIONAL_PROPS = ["x", "y", "width", "height"];
let LABEL_COUNT = 1;

export default {
  props: {
    main: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: "",
    },
    url: {
      type: String,
    },
    visible: {
      type: Boolean,
      default: false,
    },
    width: {
      type: Number,
      default: -1,
    },
    height: {
      type: Number,
      default: -1,
    },
    x: {
      type: Number,
      default: -1,
    },
    y: {
      type: Number,
      default: -1,
    },
    options: {
      type: Object,
      default: () => ({}),
    },
    preventClose: {
      type: Boolean,
      default: false,
    },
  },
  emits: [
    "created",
    "closed",
    "fileDrop",
    "focusChanged",
    "menuClicked",
    "moved",
    "resized",
    "scaleChanged",
    "themeChanged",
  ],
  setup(props, { emit, expose }) {
    const position = ref([0, 0]);
    const size = ref([0, 0]);
    const scaleFactor = ref(1);

    const window_id = `tauri_window_label_${LABEL_COUNT++}`;
    const initialSettings = {
      ...props.options,
      url: props.url,
      title: props.title,
      visible: props.visible,
    };
    // Add optional props
    for (let i = 0; i < OPTIONAL_PROPS.length; i++) {
      const key = OPTIONAL_PROPS[i];
      if (props[key] > 0) {
        initialSettings[key] = Number(props[key]);
      }
    }
    const webView = props.main
      ? appWindow
      : new WebviewWindow(window_id, initialSettings);
    const subscriptions = [];

    // Vue life cycles

    onBeforeUnmount(() => {
      while (subscriptions.length) {
        subscriptions.pop()();
      }
      hide();
      close();
    });

    // Event handling

    if (props.main) {
      webView.scaleFactor().then((scale) => {
        scaleFactor.value = scale;
        webView.outerPosition().then((p) => {
          const l = p.toLogical(scale);
          position.value = [l.x, l.y];
        });
        webView.outerSize().then((wh) => {
          const l = wh.toLogical(scale);
          size.value = [l.width, l.height];
        });
      });
    } else {
      webView.once("tauri://created", async () => {
        scaleFactor.value = await webView.scaleFactor();
        const op = (await webView.outerPosition()).toLogical(scaleFactor.value);
        const os = (await webView.outerSize()).toLogical(scaleFactor.value);
        position.value = [op.x, op.y];
        size.value = [os.width, os.height];
        emit("created", {
          scaleFactor: scaleFactor.value,
          position: position.value,
          size: size.value,
        });
      });
    }

    webView.once("tauri://error", function (e) {
      console.error("Tauri window error");
      console.error(e);
    });

    subscriptions.push(
      webView.onCloseRequested((event) => {
        emit("closed");
        if (props.preventClose) {
          event.preventDefault();
        }
      })
    );
    subscriptions.push(
      webView.onFileDropEvent((event) => {
        emit("fileDrop", event);
      })
    );
    subscriptions.push(
      webView.onFocusChanged(({ payload: focused }) => {
        emit("focusChanged", focused);
      })
    );
    subscriptions.push(
      webView.onMenuClicked(({ payload: menuId }) => {
        emit("menuClicked", menuId);
      })
    );
    subscriptions.push(
      webView.onMoved(async ({ payload }) => {
        const logical = payload.toLogical(scaleFactor.value);
        const data = [logical.x, logical.y];
        position.value = data;
        emit("moved", data);
      })
    );
    subscriptions.push(
      webView.onResized(({ payload }) => {
        const logical = payload.toLogical(scaleFactor.value);
        size.value = [logical.width, logical.height];
        emit("resized", size.value);
      })
    );
    subscriptions.push(
      webView.onScaleChanged(({ payload }) => {
        scaleFactor.value = payload.scaleFactor;
        emit("scaleChanged", payload.scaleFactor);
      })
    );
    subscriptions.push(
      webView.onThemeChanged(({ payload }) => {
        emit("themeChanged", payload);
      })
    );

    // Reactive props

    watch(() => props.title, setTitle);
    watch(
      () => [props.x, props.y],
      (xy) => setPosition(xy[0], xy[1])
    );
    watch(
      () => [props.width, props.height],
      (wh) => setSize(wh[0], wh[1])
    );
    watch(
      () => props.visible,
      (v) => (v ? show : hide)()
    );

    // Public API

    function getWebWindow() {
      return webView;
    }
    function center() {
      return getWebWindow().center();
    }
    function close() {
      return getWebWindow().close();
    }
    function show() {
      return getWebWindow().show();
    }
    function hide() {
      return getWebWindow().hide();
    }
    function maximize() {
      return getWebWindow().maximize();
    }
    function unmaximize() {
      return getWebWindow().unmaximize();
    }
    function minimize() {
      return getWebWindow().minimize();
    }
    function unminimize() {
      return getWebWindow().unminimize();
    }
    function grabFocus() {
      return getWebWindow().setFocus();
    }
    function setFullscreen(fullScreen = true) {
      return getWebWindow().setFullscreen(fullScreen);
    }
    function requestUserAttention(mode = null) {
      return getWebWindow().requestUserAttention(mode);
    }
    function setPosition(x, y) {
      return getWebWindow().setPosition(new LogicalPosition(x, y));
    }
    function setSize(width, height) {
      return getWebWindow().setSize(new LogicalSize(width, height));
    }
    function setTitle(title) {
      return getWebWindow().setTitle(title);
    }

    const api = {
      getWebWindow,
      center,
      close,
      show,
      hide,
      maximize,
      unmaximize,
      minimize,
      unminimize,
      requestUserAttention,
      grabFocus,
      setFullscreen,
      setPosition,
      setSize,
      setTitle,
    };

    expose(api);

    return {
      getWebWindow,
      api,
      position,
      size,
      scaleFactor,
    };
  },
  template: `
    <slot
      :webWindow="getWebWindow()"
      :api="api"
      :position="position"
      :size="size"
      :scaleFactor="scaleFactor"
    />`,
};
