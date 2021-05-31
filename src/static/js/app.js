$(() => {
    const debug = true;
    
    // handle join poll
    $('#addressSearchForm').on('submit', (e) => {
        e.preventDefault();
        let domain = location.hostname;
        let port = location.port;
        let protocol = location.protocol;
        let relativeFormUrl = 'participants/en/join/poll/';
        let formData = {}
        let fullUrl = `${protocol}//${domain}:${port}/${relativeFormUrl}`;

        console.log(fullUrl);

        $('#addressSearchForm').serializeArray().map( (field) => {
            formData[field.name] = field.value;
        })
        $('#pollAddress').val('');
        console.log(formData)

        fetch(fullUrl, {
            body: JSON.stringify(formData),
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formData['csrfmiddlewaretoken'] 
            }
        })
        .then( res => res.json())
        .then( res => {
            alert(res.data)
            location.reload()
        })
        .catch( err => console.log('error getting response form server', err))
    })


    function sendFetchForm(){}
})