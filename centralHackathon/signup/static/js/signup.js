document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('send-verification').addEventListener('click', function() {
        const email = document.querySelector('input[name="email"]').value;
        
        fetch('/send_verification_email/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: new URLSearchParams({
                'email': email
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
        });
    });

    document.getElementById('verify-code').addEventListener('click', function() {
        const verificationCode = document.getElementById('verification_code').value;
        
        fetch('/verify_code/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: new URLSearchParams({
                'verification_code': verificationCode
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                document.getElementById('signup-button').disabled = false; // 인증 성공 시 회원가입 버튼 활성화
            } else {
                alert(data.error);
            }
        });
    });

    document.getElementById('signup-form').addEventListener('submit', function(event) {
        if (document.getElementById('signup-button').disabled) {
            event.preventDefault(); // 인증이 완료되지 않은 경우 폼 제출 방지
            alert('인증이 완료되지 않았습니다.');
        }
    });
});

// CSRF 토큰을 가져오는 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // 쿠키가 주어진 이름으로 시작하는지 확인
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}