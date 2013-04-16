var Rates = Rates || {};

(function($, window, document, undefined){
  $(document).ready(function(){

      var currency1 = $('.currency1').val();
      var currency2 = $('.currency2').val();
      var pairs = [];
          
      var query = 'SELECT * FROM yahoo.finance.xchange WHERE pair in (';
      
      $('.currency').each(function(){
        query += '"USD' + $(this).data('code') + '"';
        
        if($(this).index() != ($('.currency').size() -1)){
          query += ',';        
        }
      });
      
      query += ')';
      console.log(query);
      
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
  
  Rates = {
    aef_handler: function(data){
      var rates = data.query.results.rate;
      var sum = 0;
      for(i=0;i<rates.length;i++){
        if(rates[i].Rate < 1){
          sum += parseFloat($('.currency').eq(i).data('amount'));
        } else {
          sum += (parseFloat(rates[i].Rate) * parseFloat($('.currency').eq(i).data('amount')));
        }
      }
      $('.balance .sum').text(sum);
    },
    rate: 0
    
  }
})(jQuery, window, document, undefined);