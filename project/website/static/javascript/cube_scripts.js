const topBar = document.getElementById('topBar');
const menuIcon = document.getElementById('menuIcon');
const menu = document.getElementById('menu');

const cubeContainer = document.getElementById('cubeContainer');
const cube = document.getElementById('cube');
const outerContainer = document.getElementById('outerContainer');

let container = document.querySelector('.cube-container');
let currentFace = 'front';

let isExpanded = false;

const frontFace = document.getElementById('frontFace');


//Tätä käytetään kuution suurentamiseen ja pienentämiseen
function toggleResize(width) {
    isExpanded = !isExpanded;
    cubeContainer.style.minWidth = '400px';
    if (isExpanded) {
        cubeContainer.style.height = frontFace.scrollHeight + 'px';
        cubeContainer.style.width = `${width}`;
    } else {
        cubeContainer.style.height = '400px';
        cubeContainer.style.width = '400px';
    }
}

//Jos käyttäjä klikkaa selaimen 'edellinen sivu' tai 'seuraava sivu' -painiketta, ladataan uudestaan sivu jolle palataan
//(Varmistaaksemme animaatioiden haluttu toiminta)
document.addEventListener("DOMContentLoaded", function() {
    window.onpageshow = function(event) {
        if (event.persisted) {
            window.location.reload();
        }
    };
});

//Tämä ajetaan avattaessa sivu. Lähinnä muutetaan kuution mittoja sivusta riippuen.
document.addEventListener("DOMContentLoaded", function() {
    const bodyID = document.body.id;
    if (bodyID == 'data_page') {
        const searchContainer = document.querySelector('.search-container');
        const tableWrapper = document.querySelector('.table-wrapper');
        setTimeout(() => {
            tableWrapper.style.opacity = 1;
        }, 1400); 
        setTimeout(() => {
            searchContainer.style.opacity = 1;
        }, 1400); 
        setTimeout(function() {
            toggleResize('70vw');
            cubeContainer.style.height = '500px';
        }, 1800);
    }
    
    else if (bodyID == 'account_page') {
        setTimeout(function() {
            toggleResize('40vw');
        }, 1400);
    }
    else if (bodyID == 'admin_page') {
        const newRadio = document.getElementById('new');
        const notNewRadio = document.getElementById('not-new');
        const newContent = document.getElementById('newFields');
        const notNewContent = document.getElementById('notNewFields');
        const defaultContent = document.getElementById('defaultContent');
        setTimeout(function() {
            toggleResize('40vw');
            outerContainer.classList.add('extra-padding');
            defaultHeight = defaultContent.scrollHeight + 100;
            
        }, 1400);
            
        newRadio.addEventListener('change', function() {
            if (this.checked) {
                var newContentHeight = newContent.scrollHeight;
                defaultHeight = parseInt(defaultHeight, 10);
                newContentHeight = parseInt(newContentHeight, 10);
                var newHeight = newContentHeight + defaultHeight;
                newHeight = newHeight.toString();
                cubeContainer.style.height = newHeight + 'px';
            }
            
        });
        
        notNewRadio.addEventListener('change', function() {
            if (this.checked) {
                var notNewContentHeight = notNewContent.scrollHeight;
                defaultHeight = parseInt(defaultHeight, 10);
                notNewContentHeight = parseInt(notNewContentHeight, 10);
                var newHeight = notNewContentHeight + defaultHeight;
                newHeight = newHeight.toString();
                cubeContainer.style.height = newHeight + 'px';
            }
        });
    }
    else if (bodyID == 'create_page') {
        const newRadio = document.getElementById('new');
        const notNewRadio = document.getElementById('not-new');
        const newContent = document.getElementById('newFields');
        const notNewContent = document.getElementById('notNewFields');
        const defaultContent = document.getElementById('defaultContent');
    
        setTimeout(function() {
            toggleResize('40vw');
            outerContainer.classList.add('extra-padding');

            defaultHeight = defaultContent.scrollHeight + 80;
            
        }, 1400);
            
        newRadio.addEventListener('change', function() {
            if (this.checked) {
                var newContentHeight = newContent.scrollHeight;
                defaultHeight = parseInt(defaultHeight, 10);
                newContentHeight = parseInt(newContentHeight, 10);
                var newHeight = newContentHeight + defaultHeight;
                newHeight = newHeight.toString();
                cubeContainer.style.height = newHeight + 'px';
            }
            
        });
        
        notNewRadio.addEventListener('change', function() {
            if (this.checked) {
                var notNewContentHeight = notNewContent.scrollHeight;
                defaultHeight = parseInt(defaultHeight, 10);
                notNewContentHeight = parseInt(notNewContentHeight, 10);
                var newHeight = notNewContentHeight + defaultHeight;
                newHeight = newHeight.toString();
                cubeContainer.style.height = newHeight + 'px';
            }
        });
        
    }
    else if (bodyID == 'infoedit_page') {
        setTimeout(function() {
            toggleResize('40vw');
            outerContainer.classList.add('extra-padding');
        }, 1400);
    }
    else if (bodyID == 'generatedlink_page') {
        setTimeout(function() {
            toggleResize('40vw');
        }, 1400);
    }
});

//Näyttää valikon
function toggleMenu() {
    topBar.classList.toggle('show-menu');
}

//Piilottaa valikon
document.addEventListener('click', function(event) {
    if (!menu.contains(event.target) && !menuIcon.contains(event.target) && topBar.classList.contains('show-menu')) {
        topBar.classList.remove('show-menu');
    }
});

//Ajetaan, kun klikataan painikkeita, joilla siirryttäisiin toiselle sivulle – odotetaan ensin 
//animaatioiden saattamista loppuun, ja sitten siirretään käyttäjä sivulle, jonne hän oli menossa
function handleButtonClick(event, link) {
    const sivu = window.location.pathname;
    if (`${sivu}` == '/') {
        const searchContainer = document.querySelector('.search-container');
        const tableWrapper = document.querySelector('.table-wrapper');
        if (tableWrapper.style.opacity != 0) {
            setTimeout(() => {
            tableWrapper.style.opacity = 0;
            }, 500); 
        }
        if (searchContainer.style.opacity != 0) {
            setTimeout(() => {
            searchContainer.style.opacity = 0;
            }, 500); 
        }
    }
    if (isExpanded) {
        event.preventDefault(); 
        cubeContainer.style.height = '400px';
        cubeContainer.style.width = '400px';
        setTimeout(function() {
            rotateCube('bottom');
        }, 1500); 
        setTimeout(() => {
            window.location.href = `${link}`;
        }, 2700); 
    }
    else {
        event.preventDefault();
        rotateCube('bottom');
        setTimeout(() => {
            window.location.href = `${link}`;
        }, 2400); 
    }
}

//Tätä käyttäen kuutiota pyöritellään haluttuun suuntaan
function rotateCube(side) {
    switch (side) {
        case 'front':
            cube.style.transform = 'rotateY(0deg)';
            break;
        case 'back':
            cube.style.transform = 'rotateY(180deg)';
            break;
        case 'right':
            cube.style.transform = 'rotateY(90deg)';
            break;
        case 'left':
            cube.style.transform = 'rotateY(-90deg)';
            break;
        case 'top':
            cube.style.transform = 'rotateX(90deg)';
            break;
        case 'bottom':
            cube.style.transform = 'rotateX(-90deg)';
            break;
    }
}

//Tämä ajetaan, kun painetaan submit-painiketta – odotetaan animaation saattamista loppuun, ja sitten
//submitataan
function handleSubmit(event, formID) {
    if (isExpanded) {
        event.preventDefault(); 
        cubeContainer.style.height = '400px';
        cubeContainer.style.width = '400px';
        setTimeout(function() {
            rotateCube('bottom');
        }, 1000); 
        setTimeout(() => {
            document.getElementById(formID).submit();
        }, 2000); 
    }
    else {
        event.preventDefault();
        rotateCube('bottom');
        setTimeout(() => {
            document.getElementById(formID).submit();
        }, 1000); 
    }

}

//Tämä on painikkeiden klikkausten erityistapausta, 'Lisätietoja/Muokkaa' -painiketta varten.
function openInfoEdit(event) {
    var itemID = document.getElementById('itemIDSelected').value;
    if (itemID) {
        
        const sivu = window.location.pathname;
        if (`${sivu}` == '/') {
            const searchContainer = document.querySelector('.search-container');
            const tableWrapper = document.querySelector('.table-wrapper');
            if (tableWrapper.style.opacity != 0) {
                setTimeout(() => {
                tableWrapper.style.opacity = 0;
                }, 500); 
            }
            if (searchContainer.style.opacity != 0) {
                setTimeout(() => {
                searchContainer.style.opacity = 0;
                }, 500); 
            }
        }
        if (isExpanded) {
            cubeContainer.style.height = '400px';
            cubeContainer.style.width = '400px';
            setTimeout(function() {
                rotateCube('bottom');
            }, 1500); 
            setTimeout(() => {
                window.location.href = `/info_edit?id=${itemID}`;
            }, 2700); 
        }
        else {
            rotateCube('bottom');
            setTimeout(() => {
                window.location.href = `/info_edit?id=${itemID}`;
            }, 2400); 
        }

    } else {
        alert("Valitse ensin jokin tavara.");
    }
}