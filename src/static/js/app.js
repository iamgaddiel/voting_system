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

        $('#addressSearchForm').serializeArray().forEach((field) => formData[field.name] = field.value);
        $('#pollAddress').val('');

        // check for account type
        if (formData.account_type === 'participant') relPath = 'participants/en/join/poll/';
        if (formData.account_type === 'judge') relPath = 'judges/en/join/poll/';

        let endPoint = `${baseUrl}${relPath}`;
        let response = await submitForm(endPoint, formData);
        location.reload()
    })

    // upload project link
    $('#projectLinkForm').on('submit', async (event) => {
        event.preventDefault();
        let endPoint = `${baseUrl}participants/en/project/link/upload/`;
        let formData = {};

        $('#projectLinkForm').serializeArray().map((field) => {
            formData[field.name] = field.value;
        })

        let response = await submitForm(endPoint, formData);
        alert(response.data);
        location.reload();
    })

    // get participant details
    $('.participantLink').on('click', async (event) => {
        event.preventDefault();
        const userId = event.currentTarget.getAttribute('data-id');
        const pollAddress = event.currentTarget.getAttribute('data-poll');
        const endPoint = `${baseUrl}judges/en/get/participant/detail/${userId}/${pollAddress}`;
        const { data } = await fetchData(endPoint);
        const fullName = `${data.first_name} ${data.last_name}`;

        // display voted on the voted participant
        if (data.voted && data.voted_participant) {
            $('#voteBtn')
                .attr({ 'disabled': true, 'class': 'btn btn-secondary' })
                .html('<i class="fas fa-thumbs-up"></i> you\'ve voted')
                .css({ 'display': 'block' })
            $('#rating-wrapper').css({'display': 'none'})
        }
        // else {
        //     $('#voteBtn').css({ 'display': 'none' })
        // }
        $('#participantName').html(fullName);
        $('#participantEmail').html(data.email);
        $('#participantStack').html(data.stack);
        $('#participantProjectLink').html(data.project_link || 'unavailable');
        document.querySelector('#vp-id').setAttribute('value', data.participant_id)
        document.querySelector('#participantProjectLink').setAttribute('href', data.project_link);
    })

    // vote for a participant
    $('#voteForm').on('submit', async (event) => {
        event.preventDefault()
        let formData = {};
        const endPoint = `${baseUrl}judges/en/vote/participant/`
        const voteBtn = $('#voteBtn');
        $('#voteForm').serializeArray().map(field => formData[field.name] = field.value);
        try {
            let response = await submitForm(endPoint, formData);
            alert(response.data)
        } catch (err) {
            console.log(err)
        }
        $(voteBtn)
            .attr({ 'disabled': true, 'class': 'btn btn-secondary' })
            .html('<i class="fas fa-thumbs-up"></i> you\'ve voted')
    })


    // update score value label
    $('#ratingValue').on('change', displayVoteRating) 
    $('#ratingValue').on('input', displayVoteRating) 

// ====================================== [ Functions ] =========================================
    // update score value label
    function displayVoteRating(){
        $('#ratingValueLabel').html(this.value)
    }

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
