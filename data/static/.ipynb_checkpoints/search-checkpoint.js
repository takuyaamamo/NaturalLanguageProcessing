let main = new Vue({
  el: '#main',//<div id="main">...</div>に対応する
  // 下記で変数定義
  data: {
    keywords: '魚',//<input type="text" v-model="keywords" />に対応しテキストフィールドの中の文字列を表す。
    result: [],//<div>{{ result }}</div>に対応し、div中の変数に該当する
    hl: {},
  },

  methods: {
    // 下記はv-on:click="run"に対応し,Searchボタンが押された時に実行される
    run: function() {
      //Vue.jsの関数でサーバサイドにリクエストを投げる関数のthis.$http.get('/get'...)によりhttp://localhost:8702/getにパラメータとしてkeywordsリクエストを投げる
      this.$http.get(
        '/get',
        {"params": { 'keywords': this.keywords, }},
      ).then(response => {
        // this.result = response.body.responseによりサーバーサイドから返されたJSONのresponseの値をresult変数に代入する。これがそのまま<div>{{ result }}</div>に表示される
        this.result = response.body.response;
        this.hl = response.body.highlighting;
      }, response => {
        console.log("NG");
        consle.log(response.body);
      });
    },
  }
});