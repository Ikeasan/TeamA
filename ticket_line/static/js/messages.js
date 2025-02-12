// 一定時間後にメッセージをフェードアウト
document.addEventListener("DOMContentLoaded", function() {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.5s ease-out";
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 500);
        }, 3000); // 3秒後にフェードアウト
    });
});

function toggleSubmitButton() {
    const agreementCheckbox = document.getElementById("agreement");
    const submitButton = document.getElementById("submit-button");

    // チェックボックスの状態に応じてボタンを有効化/無効化
    if (agreementCheckbox.checked) {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}

function handleSubmit() {
    const agreementCheckbox = document.getElementById("agreement");

    // チェックされていない場合、アラートを表示して処理を中断
    if (!agreementCheckbox.checked) {
        alert("利用規約と注意事項に同意してください。");
        return;
    }

    // チェックされている場合、フォームを送信
    document.querySelector("form").submit();
}
