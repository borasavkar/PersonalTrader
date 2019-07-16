var options = {
    url: "static/json/ticker.json",
    
  
      getValue: function(element) {
          return element.Code + ' - ' + element.Name;
      },
  
      template: {
          type: "description",
          fields: {
              description: "Exchange"
          }
      },
      
      list: {
          onSelectItemEvent: function() {
              var selectedItemName= $("#provider-json").getSelectedItemData().Name;
              var selectedItemCode= $("#provider-json").getSelectedItemData().Code;
  
              $("#basics").val(selectedItemName).trigger("change");
              $("#provider-json").val(selectedItemCode).trigger("change");
              $("#code").val(selectedItemCode).trigger("change");
          },

          match: {
              enabled: true
          }
    },
    
  };
  
$("#provider-json").easyAutocomplete(options);
