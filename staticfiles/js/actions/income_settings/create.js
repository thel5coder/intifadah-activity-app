async function createSetting() {
    const btn = $('#btnSaveSetting')
    btn.disabled = true
    btn.textContent = "Menyimpan..."

    const response = axios.post('/income/setting/create', {
        key: $('#id_key').val(),
        val: $('#id_value').val(),
        type: $('#id_type').val()
    }).then(response => {
        btn.disabled = false
        btn.textContent = "Simpan"
        console.log(response)
    }).catch(error => {
        btn.disabled = false
        btn.textContent = "Simpan"
        console.log(error)
    })
}