$(() => {
    const debug = true;
    
    // handle join poll
    $('#addressSearchForm').on('submit', (e) => {
        e.preventDefault();
        let domain = location.hostname;
        let port = location.port;
        let protocol = location.protocol;
        let relativeFormUrl = '';
        let formData = {};
        
        
        // check for account type
        $('#addressSearchForm').serializeArray().forEach((field) => formData[field.name] = field.value);
        $('#pollAddress').val('');
        console.log(FormData); // todo: remove this line

        console.log(formData.account_type); // todo: remove this line
        if (formData.account_type === 'participant') relativeFormUrl = 'participants/en/join/poll/';
        if(formData.account_type === 'judge') relativeFormUrl = 'judges/en/join/poll/';
        
        let fullUrl = `${protocol}//${domain}:${port}/${relativeFormUrl}`;
        console.log(fullUrl); // todo: remove this line


        fetch(fullUrl, {
            body: JSON.stringify(formData),
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formData['csrfmiddlewaretoken']
            }
        })
            .then(res => res.json())
            .then(res => {
                alert(res.data)
                location.reload()
            })
            .catch(err => console.log('error getting response form server', err))
    })

    $('#projectLinkForm').on('submit', (event) => {
        event.preventDefault();
        let domain = location.hostname;
        let port = location.port;
        let protocol = location.protocol;
        let relativeFormUrl = 'participants/en/project/link/upload/';
        let fullUrl = `${protocol}//${domain}:${port}/${relativeFormUrl}`;

        $('#projectLinkForm').serializeArray().map((field) => {
            formData[field.name] = field.value;
        })

        console.log(FormData);

        fetch(fullUrl, {
            body: JSON.stringify(formData),
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formData['csrfmiddlewaretoken']
            }
        })
            .then(res => res.json())
            .then(res => {
                alert(res.data)
                location.reload()
            })
            .catch(err => console.log('error getting response form server', err))
    })

    function fetchAPI(relPath, formDa) {
        let domain = location.hostname;
        let port = location.port;
        let protocol = location.protocol;
        let fullUrl = `${protocol}//${domain}:${port}/${relPath}`;

        $('#addressSearchForm').serializeArray().map((field) => {
            formData[field.name] = field.value;
        })

        fetch(fullUrl, {
            body: JSON.stringify(formData),
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formData['csrfmiddlewaretoken']
            }
        })
            .then(res => res.json())
            .then(res => {
                alert(res.data)
                location.reload()
            })
            .catch(err => console.log('error getting response form server', err))
    }
})
