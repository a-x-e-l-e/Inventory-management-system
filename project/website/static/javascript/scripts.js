//Tätä käytetään tietokannan selailunäkymässä rivin valintaan
document.addEventListener("DOMContentLoaded", function() {
    const tableRows = document.querySelectorAll(".table-row");

    tableRows.forEach(function(row) {
        row.addEventListener("click", function() {
            tableRows.forEach(function(row) {
                row.classList.remove("selected");
            });

            row.classList.add("selected");
        });
    });
});

//Tätä käytetään text inputien required-attribuutin hallintaan
function toggleRequiredInputs(required) {
    document.querySelectorAll('#new-inputs input').forEach(input => {
        input.required = required;
    });
}

//Ja tätä taas dropdownin required-attribuutin hallintaan
function toggleRequiredDropdown(required) {
    document.querySelector('#dropdown select').required = required;
}

//Tätä käytetään create_new.html -sivulla elementtien piilottamiseen ja näyttämiseen sen mukaan, mikä radionappula on valittuna.
document.addEventListener("DOMContentLoaded", function() {
    const newRadio = document.getElementById('new');
    const notNewRadio = document.getElementById('not-new');
    const newFields = document.getElementById('newFields');
    const notNewFields = document.getElementById('notNewFields');

    const radio = document.getElementsByName('radio-buttons');

    newRadio.addEventListener('change', function() {
        if (this.checked) {
            newFields.style.display = 'block';
            notNewFields.style.display = 'none';
            toggleRequiredInputs(true); 
            toggleRequiredDropdown(false); 
        }
    });
    
    notNewRadio.addEventListener('change', function() {
        if (this.checked) {
            notNewFields.style.display = 'block';
            newFields.style.display = 'none';
            toggleRequiredInputs(false); 
            toggleRequiredDropdown(true); 
        }
    });

    if (radio[0].checked) {
        newFields.style.display = 'block';
        notNewFields.style.display = 'none';
        toggleRequiredInputs(true); 
        toggleRequiredDropdown(false); 
    }
    else if (radio[1].checked) {
        notNewFields.style.display = 'block';
        newFields.style.display = 'none';
        toggleRequiredInputs(false); 
        toggleRequiredDropdown(true); 
    }
});


//Kun jotakin selailunäkymän tavaraa klikataan, sen ID asetetaan kahteen näkymättömään kenttään,
//joiden avulla sitten tavaraa voidaan tarkastella/muokata, tai se voidaan poistaa
function getItemID(element) {
    var itemID = element.dataset.id;
    document.getElementById('itemIDSelected').value = itemID;
}

//Käytetään kun tavara halutaan poistaa. Estetään submit jos mitään ei ole valittu.
function validateSelection(event) {
    var itemID = document.getElementById('itemIDSelected').value;
    if (!itemID) {
        event.preventDefault();
        alert('Valitse ensin poistettava tavara.');
    }
}


//Flaskin flash-messaget katoavat viiden sekunnin kuluttua ilmestymisestään
document.addEventListener('DOMContentLoaded', (event) => {
    const flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(message => {
                message.style.transition = 'opacity 0.5s ease-out';
                message.style.opacity = '0';
                setTimeout(() => {
                    message.remove();
                }, 500);
            });
        }, 3000); 
    }
});

document.getElementById('back-button').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = '/';
});

document.getElementById('back-button2').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = '/';
});


//Tällä etsitään selailunäkymässä tavaroita nimen, mallin tai valmistajan perusteella
function searchFor() 
{
    var text = document.getElementById('search').value;
    const tableRows = document.querySelectorAll(".table-row");
    tableRows.forEach(function(row) {
        if (!(((String(row.querySelector('.tavaranimi').dataset.id)).toLowerCase()).includes(String(text).toLowerCase()) || 
                ((String(row.querySelector('.tavaramalli').dataset.id)).toLowerCase()).includes(String(text).toLowerCase()) ||
                ((String(row.querySelector('.tavaravalmistaja').dataset.id)).toLowerCase()).includes(String(text).toLowerCase())))
            row.style.display = "none";
        else if (row.style.display = "none" && (((String(row.querySelector('.tavaranimi').dataset.id)).toLowerCase()).includes(String(text).toLowerCase()) ||
                    ((String(row.querySelector('.tavaramalli').dataset.id)).toLowerCase()).includes(String(text).toLowerCase())  ||
                    ((String(row.querySelector('.tavaravalmistaja').dataset.id)).toLowerCase()).includes(String(text).toLowerCase())))
            row.style.display = "table-row";
    })
}





