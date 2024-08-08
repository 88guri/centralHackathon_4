document.addEventListener('DOMContentLoaded', function() {
    function updateCharacter() {
        var level = parseInt(document.getElementById('character-level').innerText, 10);
        
        // container 요소에서 데이터를 가져옴
        var container = document.querySelector('.container');
        var currentExperience = parseInt(container.getAttribute('data-current-experience'), 10);
        var maxExperience = parseInt(container.getAttribute('data-max-experience'), 10);
        var defaultImg = container.getAttribute('data-default-img');
        var childImg = container.getAttribute('data-child-img');
        var adultImg = container.getAttribute('data-adult-img');
        
        var progressBar = document.getElementById('progress-bar');
        var characterImage = document.getElementById('character-image');
        var charDiv = document.querySelector('.character-container');

        // 진행 상황 바의 너비를 레벨에 따라 조정
        var progressWidth = (currentExperience / maxExperience) * 100;
        progressBar.style.width = progressWidth + '%';

        // 캐릭터 진화 설정
        var imageSrc;
        if (level >= 30) {
            imageSrc = adultImg;
        } else if (level >= 5) {
            imageSrc = childImg;
        } else {
            imageSrc = defaultImg;
        }
        characterImage.src = imageSrc;

        // Set the class name based on the image source
        var className = imageSrc.split('/').pop().split('.')[0];
        characterImage.className = className;

        // 로컬 저장소에서 캐릭터 아이템을 로드합니다
        var charItems = JSON.parse(localStorage.getItem('charItems')) || {};

        // 현재 캐릭터 컨테이너의 기존 아이템을 지웁니다
        charDiv.querySelectorAll('img:not(#character-image)').forEach(function(img) {
            img.remove();
        });

        // 로컬 저장소에서 아이템을 적용합니다
        for (var type in charItems) {
            if (charItems.hasOwnProperty(type)) {
                var img = document.createElement('img');
                img.src = charItems[type];
                img.className = `char-${type}`;
                charDiv.appendChild(img);
            }
        }
    }

    updateCharacter(); // 처음 로드 시 데이터 업데이트

    // 데이터가 변경되었을 때 로컬 저장소에서 강제로 업데이트
    window.addEventListener('storage', function(event) {
        if (event.key === 'charItems') {
            updateCharacter();
        }
    });
});
