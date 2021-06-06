$(() => {
    const debug = true;
    const domain = location.hostname;
    const port = location.port;
    const protocol = location.protocol;
    const baseUrl = `${protocol}//${domain}:${port}/`;



    // handle join poll
    $('#addressSearchForm').on('submit', async (event) => {
        event.preventDefault();
        let relPath = '';
        let formData = {};
        let endPoint = '';
        
        
        $('#addressSearchForm').serializeArray().forEach((field) => formData[field.name] = field.value);
        $('#pollAddress').val('');
        
        if (debug) console.log($('#addressSearchForm').serializeArray()); // todo: remove this line
        if (debug) console.log(formData.account_type); // todo: remove this line

        // check for account type
        if (formData.account_type === 'participant') relPath = 'participants/en/join/poll/';
        if (formData.account_type === 'judge') relPath = 'judges/en/join/poll/';
        endPoint = `${baseUrl}${relPath}`;
        
        if (debug) console.log(endPoint); // todo: remove this line

        let response = await submitForm(endPoint, formData);

        alert(response.data)
        location.reload()
    })

    $('#projectLinkForm').on('submit', async (event) => {
        event.preventDefault();
        let relPath = 'participants/en/project/link/upload/';
        let endPoint = `${baseUrl}${relPath}`;
        let formData = {};

        $('#projectLinkForm').serializeArray().map((field) => {
            formData[field.name] = field.value;
        })

        console.log(FormData);
        let response = await submitForm(endPoint, formData);
        alert(response.data);
        location.reload();
    })

    $('.participantLink').on('click', async (event) => {
        event.preventDefault();
        const userId = event.currentTarget.getAttribute('data-id');
        const pollAddress = event.currentTarget.getAttribute('data-poll');
        const relativeUrl = `judges/en/get/participant/detail/${userId}/${pollAddress}`;
        let endPoint = `${baseUrl}${relativeUrl}`;
        const data = await fetchData(endPoint);
        const fullName = `${data.data.first_name} ${data.data.last_name}`;

        $('#participantName').html(fullName);
        $('#participantEmail').html(data.data.email);
        $('#participantStack').html(data.data.stack);
        $('#participantProjectLink').html(data.data.project_link || 'unavailable');
        document.getElementById('participantProjectLink').setAttribute('href', data.data.project_link);
    })

    async function fetchData(endPoint) {
        return (await fetch(endPoint, { method: 'GET' })).json();
    }

    async function submitForm(endPoint, formData) {
        let data = await fetch(endPoint, {
            body: JSON.stringify(formData),
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formData['csrfmiddlewaretoken']
            }
        })
        return data.json();
    }
})
