$(document).ready(function () {

            let textRejectedReason = $('#rejectedReason')
            textRejectedReason.hide()
            let score = $('#activityScoreDiv')
            score.hide()

            $('#activityStatus').change(function () {
                let selectedValue = $(this).val();
                if (selectedValue === "0") {
                    textRejectedReason.show()
                    score.show()
                } else {
                    textRejectedReason.hide()
                    score.hide()
                }
            });

        });