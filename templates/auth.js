$(document).on(
	"click",
	".commit_login",
	function () {
		var form = $(this).closest("form");

        // Navigate to auth_url
        <input type="button" onclick="window.open('http://www.example.com','_blank','resizable=yes')" />
        // if (failed)
			form.find(".help-block").removeClass("hidden");

	}
);

$(document).on("keyup change input", "input", function () {
	$(this).removeClass("input_invalid");
	$(this).closest(".form-group").find(".help-block").addClass("hidden");
});

