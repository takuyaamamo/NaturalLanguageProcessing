var hello = new Vue({
  el: '#hello',
  data: {
    namae:  '太郎',
    result: '',
  },
  methods: {
    run: function() {
      this.$http.get(
        '/get',
        {'params': {
          'namae':    this.namae,
        }},
      ).then(response => {
        console.log(response.body);
        this.result = response.body.greet;
      }, response => {
        console.log('NG');
        console.log(response.body);
      });
    },
  }
});