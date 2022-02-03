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
});

// </div>
// <div><input type="text" name="mytext[]"/>