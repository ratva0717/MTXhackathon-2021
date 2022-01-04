window.onload = () => {
    console.log("Came in");
    $("#sendbutton").click(() => {
        input = $("#imageinput")[0];
        if (input.files && input.files[0]) {

            $.ajax({
                url: "/detect", // fix this to your liking
                type: "POST",
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                error: function(data) {
                    console.log("upload error", data);
                    console.log(data.getAllResponseHeaders());
                },
                success: function(data) {
                    console.log(data);
                    // bytestring = data["status"];
                    // image = bytestring.split("'")[1];
                },
            });
        }
    });
};