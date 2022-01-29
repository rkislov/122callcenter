//  document.addEventListener('DOMContentLoaded', function() {
//      var elems = document.querySelectorAll('.datepicker');
//      var instances = M.Datepicker.init(elems, options);
//    });

  // Or with jQuery

  $(document).ready(function(){
    $('.datepicker').datepicker({
        format: 'dd.mm.yyyy',
        setDefaultDate:'01.01.1900',
        selectMonths: true,
        today: 'Сегодня',
        clear: 'Очистить',
        close: 'Закрыть',
        monthsFull: ['Январь','Февраль','Март','Апрель','Май','Июнь', 
    'Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'],
        monthsShort: ['Янв','Фев','Мар','Апр','Май','Июн', 
    'Июл','Авг','Сен','Окт','Ноя','Дек'],
        weekdaysFull: ['Воскресенье','Понедельник','Вторник','Среда','Четверг','Пятница','Суббота'],
        weekdaysShort: ['Вск','Пнд','Втр','Срд','Чтв','Птн','Сбт'],
        weekdaysLetter: [ 'В', 'П', 'В', 'С', 'Ч', 'П', 'С' ],
      });
  });
