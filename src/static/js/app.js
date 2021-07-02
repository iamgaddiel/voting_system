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
        if (data.voted) {
            $('#voteBtn')
                .attr({ 'disabled': true, 'class': 'btn btn-secondary' })
                .html('<i class="fas fa-thumbs-up"></i> you\'ve voted')
                .css({ 'display': 'block' })
            $('#rating-wrapper').css({ 'display': 'none' })
        }
        // else {
            // $('#rating-wrapper').css({ 'display': 'none' })
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
        $('#rating-wrapper').css({ 'display': 'none' })
        $(voteBtn)
            .attr({ 'disabled': true, 'class': 'btn btn-secondary' })
            .html('<i class="fas fa-thumbs-up"></i> you\'ve voted')
    })

    // update ranking

    // update score value label
    $('#ratingValue').on('change', displayVoteRating)
    $('#ratingValue').on('input', displayVoteRating)

    // update participant ranking
    // setInterval(getCurrentRanking, 3000)
    getCurrentRanking();

    // toggle show profile preview
    // $('#toggleProfile').on('click', togglePreviewProfile)
    $('#toggleProfile').click((event) => {
        event.preventDefault()
        $('.profile-preview').toggle(100)
    })


    $('#deleteAllBtn').on('click', handleDelete)  // Delete all instance of a Model
    $('#deleteBtn').on('click', handleDelete) // Delete single model instance


    // ====================================== [ Functions ] =========================================

    async function handleDelete(event) {
        event.preventDefault()
        let endPoint = $(this).attr('href')
        let confirmation = confirm('Are you sure you want to delete everything ?')
        if (confirmation) {
            await deleteAllObjects(endPoint)
            location.reload
        }
    }

    // delete all instance of model
    async function deleteObjects(endPoint) {
        return (await fetch(endPoint, { method: 'GET' })).json()
    }

    async function getCurrentRanking() {
        try {
            const pollAddress = location.pathname.split('/')[5]
            const endPoint = `${baseUrl}judges/en/get/participant/rankings/${[pollAddress]}`
            const { data, error } = await fetchData(endPoint)

            if (!data) {
                console.error(error)
            } else {
                console.log(data.poll_details)
                let scores = ''

                data.poll_details.map((
                    {
                        first_name,
                        last_name,
                        username,
                        average_rating
                    }, index) => {
                    scores += `<li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <span>${index += 1} |</span>
                            <b class="ml-5" style="margin-left: 5px;">${first_name} ${last_name} | ${username}</b>
                        </div>
                        <div>
                            <small>
                                <span>${average_rating}</span>
                            </small>
                        </div>
                    </div>
                </li>`
                })
                $('#scoreBoard').html(scores)
            }
        }
        catch (err) {
            console.error(err)
        }
    }

    // update score value label
    function displayVoteRating() {
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
