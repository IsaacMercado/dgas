/* Project specific Javascript goes here. */
$(document).ready(function() {


  // File type Select after Network selection
    function update_parroquia(_network, _type) {
        var response = $.ajax({
            async: false,
            dataType: "json",
            url: "/users/parroquias/" + _network
        }).responseText;
        response = JSON.parse(response);
        type = $("#id_parroquia");
        type.empty();
        type.append("<option value>---------</option>");
        for (var i = response.length - 1; i >= 0; i--) {
            var new_option = "<option value=\"" + response[i].id + "\">" + response[i].parroquia + "</option>";
            type.append(new_option);
        }
        type.val(_type);
    }
    if ($("#id_parroquia")) {
        network = $("#id_municipio").val();
        if (network) {
            update_parroquia(network, $("#id_parroquia").val());
        }
        else {
            type = $("#id_parroquia");
            type.empty();
            type.append("<option value>---------</option>");
        }
    }
    $("#id_municipio").change(function() {
        update_parroquia($(this).val(), "");
    });

});
