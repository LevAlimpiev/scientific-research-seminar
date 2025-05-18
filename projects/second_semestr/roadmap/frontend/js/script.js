document.addEventListener('DOMContentLoaded', function() {
    // Обработка открытия/закрытия этапов роадмапа
    const stageHeaders = document.querySelectorAll('.stage h3');
    
    stageHeaders.forEach(header => {
        // Начальное состояние: первый этап открыт, остальные закрыты
        const stageContent = header.nextElementSibling;
        const isFirstStage = header.parentElement.id === 'stage1';
        
        if (!isFirstStage) {
            stageContent.style.display = 'none';
            header.classList.add('collapsed');
        }
        
        // Добавление обработчика кликов для раскрытия/скрытия этапов
        header.addEventListener('click', function() {
            const content = this.nextElementSibling;
            
            if (content.style.display === 'none' || content.style.display === '') {
                content.style.display = 'block';
                this.classList.remove('collapsed');
                this.style.setProperty('--icon-content', '"−"');
            } else {
                content.style.display = 'none';
                this.classList.add('collapsed');
                this.style.setProperty('--icon-content', '"+"');
            }
        });
    });
    
    // Плавная прокрутка при клике по якорным ссылкам
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 20,
                    behavior: 'smooth'
                });
                
                // Если это ссылка на этап, раскроем его
                if (targetId.includes('stage')) {
                    const stageHeader = targetElement.querySelector('h3');
                    const stageContent = stageHeader.nextElementSibling;
                    
                    if (stageContent.style.display === 'none') {
                        stageContent.style.display = 'block';
                        stageHeader.classList.remove('collapsed');
                    }
                }
            }
        });
    });
    
    // Добавление активного состояния для текущего этапа при прокрутке
    window.addEventListener('scroll', function() {
        const stages = document.querySelectorAll('.stage');
        let currentStageId = '';
        
        stages.forEach(stage => {
            const rect = stage.getBoundingClientRect();
            if (rect.top <= 100 && rect.bottom >= 100) {
                currentStageId = stage.id;
            }
        });
        
        if (currentStageId) {
            document.querySelectorAll('.stage').forEach(stage => {
                stage.classList.remove('active');
            });
            document.getElementById(currentStageId).classList.add('active');
        }
    });
    
    // Добавление поиска (фильтрации) по содержимому роадмапа
    const searchInput = document.getElementById('search-roadmap');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const stages = document.querySelectorAll('.stage');
            
            stages.forEach(stage => {
                const stageContent = stage.textContent.toLowerCase();
                if (stageContent.includes(searchTerm)) {
                    stage.style.display = 'block';
                    
                    // Если есть поисковый запрос, раскрываем этапы с совпадениями
                    if (searchTerm.length > 2) {
                        const content = stage.querySelector('.stage-content');
                        content.style.display = 'block';
                    }
                } else {
                    stage.style.display = 'none';
                }
            });
        });
    }
}); 