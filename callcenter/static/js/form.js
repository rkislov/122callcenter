$(document).ready(function() {
    var max_fields      = 10; //maximum input boxes allowed
    var wrapper         = $(".add-person"); //Fields wrapper
    var add_button      = $("#add-person-form"); //Add button ID

    var x = 1; //initlal text box count
    $(add_button).click(function(e){ //on add input button click
        e.preventDefault();
        if(x < max_fields){ //max input box allowed //text box increment
            var form_idx = $('#TOTAL_FORMS').val();
            $(wrapper).append(`
           <div>
                <div class="row">
                                <div class="input-field col s6">
                                    <i class="material-icons prefix">account_circle</i>
                                    <input placeholder="Иванов Иван Иванович" id="patient_fio" type="text" class="validate" name="patient_fio[]">
                                    <label for="patient_fio">ФИО пациента</label>
                                </div>
                                <div class="input-field col s6">
                                    <i class="material-icons prefix">event</i>
                                    <input type="text" id="date2" class="datepicker" name="date_of_birth[]">
                                    <label for="date2">Дата рождения</label>
                                </div>
                              </div>
            <a href="#" class="remove_field btn-floating btn-small waves-effect waves-light red"><i class="material-icons">close</i></a></div>
            <br>`); //add input box
        }
        $('#TOTAL_FORMS').val(parseInt(form_idx) + 1);
        x++;
    });

    $(wrapper).on("click",".remove_field", function(e){ //user click on remove text
        var form_idx = $('#TOTAL_FORMS').val();
        $('#TOTAL_FORMS').val(parseInt(form_idx) -1 );
        e.preventDefault(); $(this).parent('div').remove(); x--;
    })
    
    $("#subject").change(function () {
      var url = "/ajax/load_sub_subject/";  // get the url of the `load_cities` view
      var subjectId = $(this).val();  // get the selected country ID from the HTML input

      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'subject': subjectId       // add the country id to the GET parameters
        },
        dataType: 'json',
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#id_city").html(data);  // replace the contents of the city input with the data that came from the server
        }
      });

    });
});

// </div>
// <div><input type="text" name="mytext[]"/>