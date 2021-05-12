function save_unit_modifs(unit_id){

    let formData = $("#saveUnitModifs" + unit_id).serializeArray()
    let request = makePostRequest('/saveUnitModifs', formData)
    fetch(request).then(response => response.json()).then(
        data => {
            let french_text = data['french_text']
            $('#french_text'+ unit_id).innerHTML = french_text
    })
    return
}

