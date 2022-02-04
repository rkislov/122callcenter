// document.addEventListener('DOMContentLoaded', function() {
//     var elems = document.querySelectorAll('select');
//     var instances = M.FormSelect.init(elems, options);
//   });

  // Or with jQuery

  $(document).ready(function(){
    $('select').formSelect();
    $('input#callback_number, input#call_number').characterCounter();
    $('#question').val('');
    M.textareaAutoResize($('#question'));
  });

