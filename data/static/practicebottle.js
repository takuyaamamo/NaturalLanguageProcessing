var hello = new Vue({
  el: '#hello', // el: '#hello'は<div id="hello"> ... </div>に対応している
  data: { //変数を定義
    namae:  '太郎', // namae:は<input type="text" v-model="namae"/>に対応
    result: '', // result:は<div>{{ result }}</div>に対応
  },
  methods: {
    run: function() { // run: function() { ... }の関数は<button v-on:click="run">Hello</button>に対応し、Helloボタンが押された時に実行される
      //this.$http.getはVue.jsの関数
      this.$http.get( //this.$http.get('/get', ...)によりhttp://localhost:8702/getにnamaeをパラメータとしてgetリクエストする。
        '/get',
        {'params': {
          'namae':    this.namae,
        }},
      ).then(response => { //this.result = response.body.greet;により、サーバサイドのプログラムから返されたJSONのgreetの値をresult変数に代入する。それが<div>{{ result }}</div>に表示される
        console.log(response.body);
        this.result = response.body.greet;
      }, response => {
        console.log('NG');
        console.log(response.body);
      });
    },
  }
});
