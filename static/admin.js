$("input#submitButton").click(function() {
    const projectId = $("#projectid").val()
    const apiToken = $('#apitoken').val()
    const data = {
        "projectId": projectId,
        "apiToken": apiToken
    }
    fetch("http://localhost:8095/admin/ranker/set", {
    // fetch("http://expertsearch.centralus.cloudapp.azure.com/admin/ranker/set", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    }).then(response => {
        console.log(response)
        $("#rankerSuccessDiv").append(
            `<h5 class="success-block">Ranker Successfully Uploaded</h5>`
        )
    });
});

$("#viewRankerButton").click(function() {
    fetch("http://localhost:8095/admin/ranker/get", {
    // fetch("http://expertsearch.centralus.cloudapp.azure.com/admin/ranker/get", {
    }).then(response => {
        response.json().then(data => {
            $("#rankerContentsDiv").empty()
            $("#rankerContentsDiv").append(
                `<pre class="code-block">${data.ranker_contents}</pre>`
            );
        })
    });
});