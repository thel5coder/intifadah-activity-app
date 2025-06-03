function createSetting() {
    const btn = $('#btnSaveSetting')
    btn.text("Menyimpan data...")
    btn.prop('disabled', true)

    const err = $('#errorAlert')
    const success = $('#successAlert')

    axios.post('/income/setting/create', {
        key: $('#id_key').val(),
        val: $('#id_value').val(),
        type: $('#id_type').val()
    }).then(response => {
        if (response.status === 200) {
            success.show()
            btn.text("Simpan")
            btn.prop('disabled', false)
            setTimeout(function () {
                window.location.replace('/income/setting/')
            }, 2000)
        }
    }).catch(error => {
        btn.text("Simpan")
        btn.prop('disabled', false)

        err.show()
        err.text(error.response.data.error)
        setTimeout(function () {
            err.hide()
        }, 2000)
    })
}