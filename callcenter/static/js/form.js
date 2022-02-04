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
                                    <input type="text" id="date1" class="datepicker" name="date_of_birth[]">
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

    $(document).ready
(
	function()
	{
		
		// $('#call_number').simpleMask( { 'mask': ['#(###) ###-##-##'], });
        $('#date').simpleMask( { 'mask': '##.##.####'                         ,  } );
		$('#date0').simpleMask( { 'mask': '##.##.####'                         ,  } );
        $('#date1').simpleMask( { 'mask': '##.##.####'                         ,  } );
        $('#date2').simpleMask( { 'mask': '##.##.####'                         ,  } );
        $('#date3').simpleMask( { 'mask': '##.##.####'                         ,  } );
        $('#date4').simpleMask( { 'mask': '##.##.####'                         ,  } );
		$('#frCpf' ).simpleMask( { 'mask': '###.###.###-##'                     , } );
		$('#frCallback').simpleMask
		(
			{
				'mask'       : '#####',
				'nextInput'  : true,
				'onComplete' : function(element)
				{
					console.log('onComplete', element);
				}
			}
		);
	}
);
    
});
