var Rates = Rates || {};

(function($, window, document, undefined){
  $(document).ready(function(){
    $('select').bind('change', function(){
      //TODO ajax yql url here
      var currency1 = $('.currency1').val();
      var currency2 = $('.currency2').val();
      var query = 'SELECT * FROM yahoo.finance.xchange WHERE pair in ("' + currency1 + currency2 + '")'
      var dataOptions = {
        q: query,
        format: 'json',
        diagnostics: true,
        env: 'store://datatables.org/alltableswithkeys',
        callback: 'Rates.aef_handler'
      }
      var yqlurl = 'http://query.yahooapis.com/v1/public/yql';
      
      $.ajax({url: yqlurl,
            timeout: 2000,
            data: dataOptions,
            dataType: 'jsonp',
            jsonp: false,
            jsonpCallback: 'Rates.aef_handler',
      });
      
    });
  });
  
  Rates = {
    aef_handler: function(data){
      $('.show-rate').text('');
      for(index in data.query.results.rate){
        $('.show-rate').append('<span><label>' + index + '</label>: ' + data.query.results.rate[index] + '</span>');
      }
      
    }
  }
})(jQuery, window, document, undefined);