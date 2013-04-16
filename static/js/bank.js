var Rates = Rates || {};

(function($, window, document, undefined){
  $(document).ready(function(){
    $('.max').text('(max: ' + $('.currency1 :selected').data('amount') + ')');
    $('.currency2').bind('change', function(){
      
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
    
    $('.currency1').bind('change', function(){
      $('.max').text('(max: ' + $('.currency1 :selected').data('amount') + ')');      
    });
    
    $('#tradeform :submit').bind('click', function(e){
      e.preventDefault();
           
      if(parseFloat($('.currency1 :selected').data('amount')) < parseFloat($('.amount').val())){
        alert("amount must be less than " + $('.currency1 :selected').data('amount'));        
      } else {
        var tradeurl = '/transaction'
        
        var tradeOptions = {
          old_c: $('.currency1').val(),
          new_c: $('.currency2').val(),
          rate: Rates.rate,
          amount: $('.amount').val()
        }
        $.ajax({url: tradeurl,
              timeout: 2000,
              data: tradeOptions,
              dataType: 'jsonp',
              jsonp: false,
              jsonpCallback: 'Rates.aef_handler',
        });
      }
    });
    $('.currency2').trigger('change');
  });
  
  Rates = {
    aef_handler: function(data){
      if(data.transaction_status && data.transaction_status == "success"){
        window.location.href= '/account';
      }
      $('.show-rate').text('');
      Rates.rate = data.query.results.rate.Rate;
      $('.show-rate').append('<span><label>Current Rate</label>: ' + Rates.rate + '</span>');
      
    },
    rate: 0
    
  }
})(jQuery, window, document, undefined);