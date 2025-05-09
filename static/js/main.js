// FSociety JavaScript - Created by Asero
document.addEventListener('DOMContentLoaded', function() {
    // Terminal typing animation
    const terminalElements = document.querySelectorAll('.terminal-content p.animate');
    
    if (terminalElements.length > 0) {
        terminalElements.forEach((element, index) => {
            const text = element.innerText;
            element.innerText = '';
            
            setTimeout(() => {
                let i = 0;
                const typing = setInterval(() => {
                    if (i < text.length) {
                        element.innerText += text.charAt(i);
                        i++;
                    } else {
                        clearInterval(typing);
                        element.classList.add('blinking-cursor');
                        
                        // Remove blinking cursor after a delay
                        setTimeout(() => {
                            element.classList.remove('blinking-cursor');
                        }, 3000);
                    }
                }, 50);
            }, index * 1000); // Delay each line
        });
    }
    
    // FSociety logo glitch effect
    const logo = document.querySelector('.logo');
    if (logo) {
        setInterval(() => {
            logo.classList.add('glitch');
            setTimeout(() => {
                logo.classList.remove('glitch');
            }, 200);
        }, 5000);
    }
    
    // Easter egg - Konami code
    let konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
    let konamiCodePosition = 0;
    
    document.addEventListener('keydown', function(e) {
        if (e.key === konamiCode[konamiCodePosition]) {
            konamiCodePosition++;
            
            if (konamiCodePosition === konamiCode.length) {
                activateEasterEgg();
                konamiCodePosition = 0;
            }
        } else {
            konamiCodePosition = 0;
        }
    });
    
    function activateEasterEgg() {
        document.body.style.backgroundColor = "#e50914";
        setTimeout(() => {
            document.body.style.backgroundColor = "#0a0a0a";
            alert("We are fsociety - Created by Asero");
        }, 500);
    }
    
    // API status check
    const statusElement = document.getElementById('api-status');
    if (statusElement) {
        fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                statusElement.textContent = data.message;
                statusElement.classList.add('highlight');
            })
            .catch(error => {
                console.error('API Status Error:', error);
                statusElement.textContent = 'Connection error...';
            });
    }
});
