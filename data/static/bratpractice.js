var bratLocation = './file/third/brat';

// head.jsでbrad関連ライブラリを読み込む
head.js(
  // External libraries
  bratLocation + '/client/lib/jquery-1.7.1.min.js',
  bratLocation + '/client/lib/jquery-ui.min.js',
  bratLocation + '/client/lib/jquery.svg.min.js',
  bratLocation + '/client/lib/jquery.svgdom.min.js',

  // brat helper modules
  bratLocation + '/client/src/configuration.js',
  bratLocation + '/client/src/util.js',
  bratLocation + '/client/src/annotation_log.js',
  bratLocation + '/client/lib/webfont.js',

  // brat modules
  bratLocation + '/client/src/dispatcher.js',
  bratLocation + '/client/src/url_monitor.js',
  bratLocation + '/client/src/visualizer.js'
);

var brat_dispatcher = undefined;
// head.readyでUtil.embed関数でアノテーションの表示部を作成する
head.ready(function() {
  brat_dispatcher = Util.embed('brat', {}, {'text': ''}, []);
});

var brat = new Vue({
  el: '#brat',
  data: {
  },
  methods: {
    run: function() {
      this.$http.get(
        '/get',
        {'params': {
        }},
      ).then(response => {
        // brat_dispatcher.postによりサーバーサイトのプログラムから返されたJSON形式のデータをアノテーション表示部に渡している。
        brat_dispatcher.post('collectionLoaded',
          [response.body.collection]);
        brat_dispatcher.post('requestRenderData',
          [response.body.annotation]);
      }, response => {
        console.log('NG');
        console.log(response.body);
      });
    },
  }
});
